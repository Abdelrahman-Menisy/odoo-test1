from odoo import models, fields, api, _


class RealStateProject(models.Model):
    _name = 'real.state.project'
    _description = 'Real State Projects'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string='Name', required=True, tracking=True)
    date = fields.Date(string='Date', default=fields.Date.today, tracking=True)
    location = fields.Char(string='Location', tracking=True)
    total_blocks = fields.Integer(string='Total Blocks', tracking=True)
    total_units = fields.Integer(string='Total Units', tracking=True)
    
    available_units_count = fields.Integer(string='Available Units', compute='_compute_units_count')
    sold_units_count = fields.Integer(string='Sold Units', compute='_compute_units_count')
    
    unit_ids = fields.One2many('real.state.units', 'project_id', string='Units')


    default_unit_price = fields.Float(
        string='Default Unit Price', 
        help="Default price used when no specific unit is selected",
        compute='_compute_average_unit_price',
        store=True,
        readonly=False  # This is key to make it editable
    )
    
    @api.depends('unit_ids.unit_price', 'available_units_count', 'sold_units_count')
    def _compute_average_unit_price(self):
        for project in self:
            if project.unit_ids:
                project.default_unit_price = sum(unit.unit_price for unit in project.unit_ids) / len(project.unit_ids)
            else:
                # Don't override the value if manually set and no units exist
                if not project.default_unit_price:
                    project.default_unit_price = 0.0


    
    @api.depends('unit_ids.unit_status')
    def _compute_units_count(self):
        for project in self:
            project.available_units_count = len(project.unit_ids.filtered(lambda u: u.unit_status == 'available'))
            project.sold_units_count = len(project.unit_ids.filtered(lambda u: u.unit_status == 'sold'))
            project.total_units = project.available_units_count + project.sold_units_count
