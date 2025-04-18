from odoo import api, fields, models, Command


class ProjectTask(models.Model):
    _inherit = 'project.task'

    checklist_ids = fields.Many2many('fsm.checklist', 'checklist_rel')
    visible_line_ids = fields.One2many('fsm.checklist.item.value', 'task_id', string="Visible Lines")
    state = fields.Selection(
        selection_add=[('05_return_sav', 'Return SAV')],
        ondelete={'05_return_sav': 'set default'}
    )
    def write(self, vals):
        checklist_value_model = self.env['fsm.checklist.item.value']

        for task in self:
            checklist_ops = vals.get('checklist_ids', [])
            if not checklist_ops:
                continue

            unlink_ids = [item[1] for item in checklist_ops if item[0] == 3]
            link_ids = [item[1] for item in checklist_ops if item[0] == 4]

            # 🗑️ Unlink existing values
            if unlink_ids:
                checklist_value_model.search([
                    ('task_id', '=', task.id),
                    ('checklist_id', 'in', unlink_ids)
                ]).unlink()

            # ➕ Prepare all records to be created
            if link_ids:
                records_to_create = []
                for checklist in self.env['fsm.checklist'].browse(link_ids):
                    # Add section line
                    records_to_create.append({
                        'task_id': task.id,
                        'checklist_id': checklist.id,
                        'name': checklist.name,
                        'display_type': 'line_section',
                    })

                    # Add all checklist items
                    records_to_create.extend([{
                        'task_id': task.id,
                        'item_id': item.id,
                        'checklist_id': checklist.id,
                        'display_type': 'line_item',
                    } for item in checklist.checklist_item_ids])

                checklist_value_model.create(records_to_create)

        return super().write(vals)

