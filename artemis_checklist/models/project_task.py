from odoo import api, fields, models, Command, _
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    checklist_ids = fields.Many2many('fsm.checklist', 'checklist_rel')
    visible_line_ids = fields.One2many('fsm.checklist.item.value', 'task_id', string="Visible Lines", copy=True)
    state = fields.Selection(
        selection_add=[('05_return_sav', 'Return SAV')],
        ondelete={'05_return_sav': 'set default'}
    )
    client_arrival = fields.Char(string="State of the Installation upon the client’s arrival")
    manual_fill = fields.Boolean(string="Checklist Fill Manually")
    return_sav_task = fields.Many2one('project.task')
    sav_follow_up = fields.Boolean(string="SAV Follow-Up")

    def update_checklist_item(self, vals, res):
        checklist_value_model = self.env['fsm.checklist.item.value']
        checklist_ops = vals.get('checklist_ids', [])
        if not checklist_ops:
            return False
        unlink_ids = [item[1] for item in checklist_ops if item[0] == 3]
        link_ids = [item[1] for item in checklist_ops if item[0] == 4]
        if unlink_ids:
            checklist_value_model.search([
                ('task_id', '=', res.id),
                ('checklist_id', 'in', unlink_ids)
            ]).unlink()
        if link_ids:
            records_to_create = []
            for checklist in self.env['fsm.checklist'].browse(link_ids):
                # Add section line
                records_to_create.append({
                    'task_id': res.id,
                    'checklist_id': checklist.id,
                    'name': checklist.name,
                    'display_type': 'line_section',
                })
                # Add all checklist items
                records_to_create.extend([{
                    'task_id': res.id,
                    'item_id': item.id,
                    'checklist_id': checklist.id,
                    'display_type': 'line_item',
                } for item in checklist.checklist_item_ids])
            checklist_value_model.create(records_to_create)

    def write(self, vals):
        for task in self:
            self.update_checklist_item(vals, task)
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        res = super(ProjectTask, self).create(vals_list)
        for vals in vals_list:
            self.update_checklist_item(vals, res)
        return res

    def action_fsm_validate(self, stop_running_timers=False):
        res = super().action_fsm_validate(stop_running_timers)
        stage_done = self.env["project.task.type"].search([("name", "=", "Done")])
        stage_new = self.env["project.task.type"].search([("name", "=", "New")])
        invalid_checklistitems = self.visible_line_ids.filtered(
            lambda x: x.display_type == "line_item"
        ).mapped(
            lambda x: x.selection_value or x.integer_value != 0 or x.float_value != 0
        )
        selection_value = self.visible_line_ids.filtered(
            lambda x: x.display_type == "line_item"
                      and x.selection_value
                      and x.selection_value == "bad"
        )
        print('ffffff',invalid_checklistitems,not all(invalid_checklistitems)  , )
        if invalid_checklistitems and not all(invalid_checklistitems) and not self.manual_fill:
            print('\bbbbbbbbbbb')
            raise ValidationError(_("Please complete all checklist items before marking the task as done."))
        if selection_value:
            if stage_done:
                self.update({
                    "state": "05_return_sav",
                    "sav_follow_up": True,
                    "return_sav_task":
                        self.copy(
                            {
                                "stage_id": stage_new.id if stage_new else False,
                                "date_deadline": False,
                                "planned_date_start": False,
                            }
                        )
                })
            return {
                "type": "ir.actions.act_window",
                "res_model": "project.task",
                "view_mode": "form",
                "view_id": self.env.ref("project.view_task_form2").id,
                "res_id": self.return_sav_task.id,
                "target": "current",
            }
        return res

    def action_project_task_fsm(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "project.task",
            "view_mode": "form",
            "view_id": self.env.ref("project.view_task_form2").id,
            "res_id": self.return_sav_task.id,
            "target": "current",
        }
