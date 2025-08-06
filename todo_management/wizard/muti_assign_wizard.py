from odoo import models, fields


class MultiAssign(models.TransientModel):
    _name = 'todo.multi.assign'

    task_ids = fields.Many2many('todo.tasks')
    assign_id = fields.Many2one('res.users', string='Assign To', default=lambda self: self.env.user, required=True)

    def action_assign(self):
        for task in self.task_ids:
            task.assign_to = self.assign_id
        return {'type': 'ir.actions.act_window_close'}
