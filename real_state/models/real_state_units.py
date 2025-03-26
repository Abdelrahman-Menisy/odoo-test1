from odoo import models, fields, api, _


class RealStateUnits(models.Model):
    _name = 'real.state.units'
    _description = 'Real State Units'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, tracking=True)
    ref = fields.Char(string='Reference', readonly=True, default=lambda self: _('New'))
    project_id = fields.Many2one('real.state.project', string='Project', required=True, tracking=True)
    block = fields.Char(string='Block', required=True, tracking=True)
    unit_number = fields.Char(string='Unit Number', required=True, tracking=True)
    floor = fields.Char(string='Floor', required=True, tracking=True)
    unit_type = fields.Selection([
        ('studio', 'ستوديو'),
        ('small', 'صغيرة'),
        ('medium', 'متوسطة'),
        ('large', 'كبيرة'),
        ('villa', 'فيلا'),
    ], string='Unit Type', required=True, tracking=True)
    unit_status = fields.Selection([
        ('available', 'متاحة'),
        ('reserved', 'محجوزة'),
        ('sold', 'مباعة'),
        ('rented', 'مؤجرة'),
    ], string='Unit Status', required=True, default='available', tracking=True)
    unit_price = fields.Float(string='Unit Price', required=True, tracking=True)
    unit_area = fields.Float(string='Unit Area', required=True, tracking=True)



    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('ref', _('New')) == _('New'):
                vals['ref'] = self.env['ir.sequence'].next_by_code('real.state.units') or _('New')
        return super(RealStateUnits, self).create(vals_list)

