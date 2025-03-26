from odoo import models, fields, api, _
import logging
import traceback
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


class RealState(models.Model):
    _name = 'real.state'
    _description = 'Real State'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Many2one('res.partner', string='Customer', required=True, tracking=True)
    invoice_ids = fields.One2many('account.move', 'real_state_id', string='invoice')
    created_date = fields.Date(string='Created Date', default=fields.Date.today, tracking=True)
    offer_start_date = fields.Date(string='Offer Start Date', default=fields.Date.today, tracking=True)
    order_status = fields.Selection([('draft', 'Draft'), ('in_progress', 'In Progress'), ('completed', 'Completed')], string='Order Status', default='draft', tracking=True)
    
    customer_ids = fields.One2many('res.partner', 'real_state_id', string='Related Customers')
    order_ids = fields.One2many("real.state.order.lines", "order_id", string="Lines", tracking=True)
    
    amount_untaxed = fields.Float(string='Untaxed Amount', compute='_compute_amounts', store=True)
    amount_tax = fields.Float(string='Tax Amount', compute='_compute_amounts', store=True)
    total_price = fields.Float(string='Total Price', compute='_compute_amounts', store=True)
    
    @api.depends('order_ids.price_subtotal', 'order_ids.tax_amount', 'order_ids.price_total')
    def _compute_amounts(self):
        for order in self:
            amount_untaxed = sum(line.price_subtotal for line in order.order_ids)
            amount_tax = sum(line.tax_amount for line in order.order_ids)
            order.amount_untaxed = amount_untaxed
            order.amount_tax = amount_tax
            order.total_price = amount_untaxed + amount_tax

    @api.model
    def create(self, vals):
        _logger.info(f"Create method called with vals: {vals}")
        new_record = super(RealState, self).create(vals)
        if vals.get('order_status') == 'completed':
            new_record._create_invoice()
        return new_record

    def write(self, vals):
        _logger.info(f"Write method called with vals: {vals}")

        # Prevent editing if order_status is 'completed'
        for record in self:
            if record.order_status == 'completed' and 'order_status' not in vals:
                raise ValidationError(_("You cannot modify this record because the order status is completed."))

        res = super(RealState, self).write(vals)

        if 'order_status' in vals and vals['order_status'] == 'completed':
            _logger.info("Triggering _create_invoice method")
            self._create_invoice()

        return res
        
    def _create_invoice(self):
        """ Ensure an invoice exists for the real estate order and update it if necessary """
        for record in self:
            try:
                _logger.info(f"Processing Real Estate record: {record.id}")

                # Check if an invoice already exists
                invoice = self.env['account.move'].search([
                    ('real_state_id', '=', record.id),
                    ('is_real_state', '=', True),
                    ('state', '!=', 'cancel')
                ], limit=1)

                invoice_lines = []
                for line in record.order_ids:
                    if not line.project_ids or not line.units_ids:
                        _logger.warning(f"Skipping line {line.id} - missing project or unit")
                        continue

                    invoice_lines.append((0, 0, {
                        'project_ids': line.project_ids.id if line.project_ids else False,
                        'units_ids': line.units_ids.id if line.units_ids else False,
                        'unit_price': line.unit_price,
                        'tax_percentage': line.tax_percentage,
                    }))

                if invoice:
                    # Update existing invoice
                    _logger.info(f"Updating existing invoice: {invoice.id}")
                    invoice.write({
                        'real_state_line_ids': [(5, 0, 0)] + invoice_lines  # Remove old lines and add new ones
                    })
                else:
                    # Create new invoice
                    _logger.info("Creating new invoice")
                    invoice = self.env['account.move'].create({
                        'move_type': 'out_invoice',  
                        'partner_id': record.name.id if record.name else False,
                        'real_state_id': record.id,
                        'is_real_state': True,
                        'invoice_date': fields.Date.today(),
                        'real_state_line_ids': invoice_lines
                    })
                    _logger.info(f"Invoice processed successfully: {invoice.id}")

            except Exception as e:
                _logger.error(f"Error processing invoice for record {record.id}: {str(e)}")
                _logger.error(traceback.format_exc())  # Logs the full traceback for debugging



class OrderLine(models.Model):
    _name = 'real.state.order.lines'
    _description = 'Order Lines'

    order_id = fields.Many2one("real.state", string="Order")
    project_ids = fields.Many2one("real.state.project", string="Project")
    units_ids = fields.Many2one("real.state.units", string="Unit", domain="[('project_id', '=', project_ids)]")
    
    unit_price = fields.Float(string='Unit Price', compute='_compute_unit_price', store=True, readonly=False)
    unit_area = fields.Float(related='units_ids.unit_area', string='Area')
    unit_status = fields.Selection(related='units_ids.unit_status', string='Status', readonly=True)
    
    tax_percentage = fields.Float(string='Tax (%)', default=15.0)
    tax_amount = fields.Float(string='Tax Amount', compute='_compute_tax_amount', store=True)
    price_subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)
    price_total = fields.Float(string='Total (with Tax)', compute='_compute_total', store=True)
    
    
    @api.depends('units_ids', 'project_ids')
    def _compute_unit_price(self):
        for line in self:
            if line.units_ids:
                line.unit_price = line.units_ids.unit_price
            elif line.project_ids:
                line.unit_price = line.project_ids.default_unit_price

    
    @api.depends('unit_price')
    def _compute_subtotal(self):
        for line in self:
            line.price_subtotal = line.unit_price
    
    @api.depends('price_subtotal', 'tax_percentage')
    def _compute_tax_amount(self):
        for line in self:
            line.tax_amount = line.price_subtotal * (line.tax_percentage / 100.0)
    
    @api.depends('price_subtotal', 'tax_amount')
    def _compute_total(self):
        for line in self:
            line.price_total = line.price_subtotal + line.tax_amount
    
    @api.onchange('project_ids')
    def _onchange_project(self):
        self.units_ids = False
        return {'domain': {'units_ids': [('project_id', '=', self.project_ids.id)]}}
    
    @api.onchange('units_ids')
    def _onchange_units(self):
        if self.units_ids:
            self.unit_price = self.units_ids.unit_price