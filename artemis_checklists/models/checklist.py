from odoo import api, fields, models
from odoo.addons.base.models.ir_model import FIELD_TYPES


class Checklist(models.Model):
    _name = 'fsm.checklist'
    _description = 'Checklist'

    name = fields.Char(string='Checklist Name', required=True)
    checklist_item_ids = fields.One2many('fsm.checklist.item', 'checklist_id', string='Checklist Items')


class ChecklistItemValue(models.Model):
    _name = 'fsm.checklist.item.value'
    _description = 'Checklist Value'


    task_id = fields.Many2one('project.task')
    item_id = fields.Many2one('fsm.checklist.item', string="Checklist Item")
    valuefield_ttype = fields.Selection(related='item_id.field_ttype', store=True)
    selection_value = fields.Selection([('good', 'Good'), ('n/a', 'N/A'), ('bad', 'Bad')])
    integer_value = fields.Integer()
    float_value = fields.Float()
    checklist_id = fields.Many2one('fsm.checklist', string="Checklist")

    name = fields.Char()
    display_type = fields.Selection(
        selection=[
            ('line_section', "Section"),
            ('line_item', "Item"),
        ],
        default=False)


class ChecklistItem(models.Model):
    _name = 'fsm.checklist.item'
    _description = 'Checklist Item'

    name = fields.Char(string='Name', required=True)
    checklist_type = fields.Selection(
        [('good/na/bad', 'Good / NA / Bad'), ('installation', 'Installation (mA)'), ('load', 'Load (V)'),
         ('battery', 'Battery (V)')],
        string='Checklist Type', required=True)
    field_ttype = fields.Selection(
        selection=FIELD_TYPES,
        string='Field Type',
        compute='_compute_field_type',
        store=True,
        readonly=False
    )
    checklist_id = fields.Many2one('fsm.checklist', string='Checklist')

    @api.depends('checklist_type')
    def _compute_field_type(self):
        type_map = {
            'good/na/bad': 'selection',
            'installation': 'integer',
            'load': 'float',
            'battery': 'char',
        }
        for record in self:
            record.field_ttype = type_map.get(record.checklist_type, False)
