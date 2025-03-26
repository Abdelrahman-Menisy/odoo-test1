from odoo import models, fields, api, _

class RealStateAccountMove(models.Model):
    _inherit = 'account.move'
    
    real_state_id = fields.Many2one('real.state', string='Real State')
    real_state_line_ids = fields.One2many('real.state.invoice.order.lines', 'invoice_id', string='Invoice Lines')
    
    is_real_state = fields.Boolean(string='Is Real State',
                                   help='a field to check is it an invoice for real state order or not (this field and the views that depended on comes from  real_state app)', default=False)
    
    amount_untaxed = fields.Float(string='Untaxed Amount', compute='_compute_amounts', store=True)
    amount_tax = fields.Float(string='Tax Amount', compute='_compute_amounts', store=True)
    total_price = fields.Float(string='Total Price', compute='_compute_amounts', store=True)
    
    @api.depends('real_state_line_ids.price_subtotal', 'real_state_line_ids.tax_amount', 'real_state_line_ids.price_total')
    def _compute_amounts(self):
        for order in self:
            amount_untaxed = sum(line.price_subtotal for line in order.real_state_line_ids)
            amount_tax = sum(line.tax_amount for line in order.real_state_line_ids)
            order.amount_untaxed = amount_untaxed
            order.amount_tax = amount_tax
            order.total_price = amount_untaxed + amount_tax

class RealStateOrderLine(models.Model):
    _name = 'real.state.invoice.order.lines'
    _description = 'Real State Invoice Order Lines'

    # Add display_type field
    display_type = fields.Selection([
        ('line_section', 'Section'),
        ('line_note', 'Note'),
        ('product', 'Product')
    ], default='product', required=True)

    invoice_id = fields.Many2one('account.move', string='Invoice')
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