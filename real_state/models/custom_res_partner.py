from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    real_state_id = fields.Many2one('real.state', string='Real State')