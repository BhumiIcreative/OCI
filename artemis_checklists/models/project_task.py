from odoo import api, fields, models, Command


class ProjectTask(models.Model):
    _inherit = 'project.task'

    checklist_ids = fields.Many2many('fsm.checklist', 'checklist_rel')
    visible_line_ids = fields.One2many('fsm.checklist.item.value', 'task_id', string="Visible Lines",
                                       compute='_compute_visible_lines', store=True, readonly=False)

    @api.depends('checklist_ids', 'checklist_ids.checklist_item_ids')
    def _compute_visible_lines(self):
        for task in self:
            print('\n--- Recomputing visible_line_ids (no duplicates) ---')

            # Collect selected checklist items from enabled checklists
            selected_items = self.env['fsm.checklist.item'].browse()
            for checklist in task.checklist_ids:
                selected_items |= checklist.checklist_item_ids

            selected_item_ids = selected_items.ids  # for faster comparison

            if not selected_item_ids:
                # If no checklists selected → clear all lines
                task.visible_line_ids = [(5, 0, 0)]
                print('🧹 All checklists disabled. Cleared visible lines.')
                continue

            # Existing lines still valid (their item is still selected)
            valid_existing_lines = task.visible_line_ids.filtered(
                lambda line: line.item_id.id in selected_item_ids
            )

            existing_item_ids = valid_existing_lines.mapped('item_id').ids

            # Prepare the commands list
            commands = []

            # Keep valid existing lines
            for line in valid_existing_lines:
                commands.append((4, line.id))

            # Add only new items not already present
            for item in selected_items:
                if item.id not in existing_item_ids:
                    commands.append((0, 0, {'item_id': item.id}))

            task.visible_line_ids = commands
            print('✅ Final visible_line_ids:', task.visible_line_ids)

    # @api.depends('checklist_ids', 'checklist_ids.checklist_item_ids')
    # def _compute_visible_lines(self):
    #     for task in self:
    #         print('\n--- Recomputing visible_line_ids ---')
    #
    #         # All selected items from enabled checklists
    #         selected_items = self.env['fsm.checklist.item'].browse()
    #         for checklist in task.checklist_ids:
    #             selected_items |= checklist.checklist_item_ids
    #
    #         # If no checklists selected → clear all
    #         if not selected_items:
    #             task.visible_line_ids = [(5, 0, 0)]
    #             print('🧹 No checklists selected. Cleared all visible lines.')
    #             continue
    #
    #         # Existing lines that are still valid (their item is in selected)
    #         valid_existing_lines = task.visible_line_ids.filtered(
    #             lambda line: line.item_id in selected_items
    #         )
    #
    #         # Track existing item_ids to avoid duplication
    #         existing_item_ids = valid_existing_lines.mapped('item_id').ids
    #
    #         # Commands list: re-link existing valid lines
    #         commands = [(4, line.id) for line in valid_existing_lines]
    #
    #         # Add any missing item
    #         for item in selected_items:
    #             if item.id not in existing_item_ids:
    #                 commands.append((0, 0, {'item_id': item.id}))
    #
    #         task.visible_line_ids = commands
    #         print('✅ Final visible_line_ids:', task.visible_line_ids)

    # @api.depends('checklist_ids', 'checklist_ids.checklist_item_ids')
    # def _compute_visible_lines(self):
    #     for task in self:
    #         print('\n--- Recomputing visible_line_ids (no sections) ---')
    #
    #         # All selected checklist items (flattened)
    #         selected_items = self.env['fsm.checklist.item'].browse()
    #         for checklist in task.checklist_ids:
    #             selected_items |= checklist.checklist_item_ids
    #
    #         # Filter only relevant existing lines (those that are still in selected checklists)
    #         preserved_lines = task.visible_line_ids.filtered(
    #             lambda l: l.item_id in selected_items
    #         )
    #
    #         # Track existing item_ids to avoid duplicates
    #         preserved_item_ids = preserved_lines.mapped('item_id').ids
    #
    #         # Prepare the commands: start fresh but keep relevant data
    #         commands = []
    #
    #         # Add preserved lines first (in original order)
    #         for line in preserved_lines:
    #             commands.append((4, line.id))  # Re-link existing line
    #
    #         # Add new missing checklist items
    #         for item in selected_items:
    #             if item.id not in preserved_item_ids:
    #                 commands.append((0, 0, {
    #                     'item_id': item.id,
    #                 }))
    #
    #         # Assign the final lines
    #         task.visible_line_ids = commands
    #         print('✅ Final visible_line_ids:', task.visible_line_ids)

    # @api.depends('checklist_ids', 'checklist_ids.checklist_item_ids')
    # def _compute_visible_lines(self):
    #     for task in self:
    #         print('\n--------------------------------------')
    #
    #         # All checklist items from selected checklists
    #         selected_items = self.env['fsm.checklist.item'].browse()
    #         for checklist in task.checklist_ids:
    #             selected_items |= checklist.checklist_item_ids
    #
    #         # Keep only lines that are still part of selected items
    #         relevant_lines = task.visible_line_ids.filtered(
    #             lambda line: line.item_id in selected_items
    #         )
    #
    #         # Get item_ids from already-linked relevant lines
    #         relevant_item_ids = relevant_lines.mapped('item_id').ids
    #
    #         # Clear everything, then re-add
    #         commands = [(5, 0, 0)]
    #
    #         # Add existing lines first (will show on top)
    #         for line in relevant_lines:
    #             commands.append((4, line.id))
    #
    #         # Add new lines that don't exist yet (they go to the bottom)
    #         for item in selected_items:
    #             if item.id not in relevant_item_ids:
    #                 commands.append((0, 0, {
    #                     'item_id': item.id,
    #
    #                 }))
    #
    #         # Assign all at once
    #         task.visible_line_ids = commands
    #         print('✅ Final visible_line_ids:', task.visible_line_ids)

    # @api.depends('checklist_ids', 'checklist_ids.checklist_item_ids')
    # def _compute_visible_lines(self):
    #     for task in self:
    #         print('\n--------------------------------------')
    #
    #         # Get all checklist items from selected checklists
    #         selected_items = self.env['fsm.checklist.item'].browse()
    #         for checklist in task.checklist_ids:
    #             selected_items |= checklist.checklist_item_ids
    #
    #         # Build set of item_ids already added
    #         existing_item_ids = task.visible_line_ids.mapped('item_id').ids
    #
    #         # Keep only items that are still relevant
    #         relevant_lines = task.visible_line_ids.filtered(lambda line: line.item_id.id in selected_items.ids)
    #
    #         # Start fresh and re-add only the correct ones
    #         commands = [(5, 0, 0)]  # Remove all existing entries
    #
    #         # Add back the still-relevant ones
    #         for line in relevant_lines:
    #             commands.append((4, line.id))  # Re-link existing lines
    #
    #         # Add new lines that are missing
    #         for item in selected_items:
    #             if item.id not in existing_item_ids:
    #                 commands.append((0, 0, {'item_id': item.id}))
    #
    #         task.visible_line_ids = commands
    #         print('✅ Computed visible_line_ids:', task.visible_line_ids)

    # @api.depends('checklist_ids')
    # def _compute_visible_lines(self):
    #     for task in self:
    #         print('\n--------------------------------------')
    #         existing_item_ids = task.visible_line_ids.mapped('item_id').ids
    #         values_to_add = []
    #
    #         for checklist in task.checklist_ids:
    #             for item in checklist.checklist_item_ids:
    #                 if item.id not in existing_item_ids:
    #                     values_to_add.append((0, 0, {
    #                         'item_id': item.id,
    #                     }))
    #         print('***********values_to_add',values_to_add)
    #         if values_to_add:
    #             task.visible_line_ids = [(4, val.id) for val in task.visible_line_ids] + values_to_add

    # @api.depends('checklist_ids')
    # def _compute_visible_lines(self):
    #     for task in self:
    #         print('\n\ntask:::', task)
    #         print('self.checklist_ids:::', self.checklist_ids.checklist_item_ids)
    #         if not self.checklist_ids:
    #             self.visible_line_ids = False
    #             return
    #         else:
    #             for item in self.checklist_ids.checklist_item_ids:
    #                 print('\n----checklist_ids------', self.checklist_ids.checklist_item_ids)
    #                 print('------item', self.visible_line_ids.item_id)
    #                 self.env['fsm.checklist.item.value'].create({
    #                     "item_id": item.id
    #                 })
    #                 # self.update({'visible_line_ids': [(0, 0, {})]})

            # # Create a set for current visible item_ids to prevent duplicates
            # current_visible_ids = set(self.visible_line_ids.mapped('item_id'))
            #
            # # Track new items to be added
            # new_items = []
            #
            # for item in self.checklist_ids.checklist_item_ids:
            #     print('self.checklist_ids.checklist_item_ids:::', self.checklist_ids.checklist_item_ids)
            #     print('self.visible_line_ids.item_id:::', self.visible_line_ids.mapped('item_id'))
            #
            #     # If item is not already in visible_line_ids, prepare to add it
            #     if item.id not in current_visible_ids:
            #         print('Adding new item:', item.id)
            #         new_items.append((0, 0, {"item_id": item.id}))
            #
            # # Only update visible_line_ids if there are new items
            # if new_items:
            #     self.visible_line_ids = [(0, 0, {"item_id": item.id}) for item in new_items]
            #
            # print('Updated visible_line_ids:', self.visible_line_ids)
