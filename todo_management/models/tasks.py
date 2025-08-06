from odoo import models, fields, api
from odoo.exceptions import ValidationError, AccessError


class Task(models.Model):
    _name = 'todo.tasks'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Task'

    ref = fields.Char(default = 'New', readonly = True, tracking=1)
    name = fields.Char('Task Name', required=True, tracking=1)
    description = fields.Text(required=True, tracking=1)
    assign_to = fields.Many2one('res.users', default=lambda self: self.env.user, required=True)
    due_date = fields.Date(required=True, tracking=1)
    is_late = fields.Boolean()
    estimated_time = fields.Integer('Estimated Time (hours)', required=True, tracking=1)
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('closed', 'closed')
    ], default='new', required=True, tracking=1)
    active = fields.Boolean(default=True)
    task_line_ids = fields.One2many('todo.task.line', 'task_id')
    total_time = fields.Integer(compute='_compute_total_time', store=True)

    @api.model
    def create(self, vals):
        task = super(Task, self).create(vals)
        if task.ref == 'New':
            task.ref = self.env['ir.sequence'].next_by_code('tasks_seq')
        return task

    @api.model
    def write(self, vals):
        user = self.env.user

        if user.has_group('todo_management.todo_user_group'):
            allowed_fields = {'state'}

            if any(field not in allowed_fields for field in vals.keys()):
                raise AccessError("User does not have permission to modify this task.")

            if 'state' in vals:
                for task in self:
                    current_state = task.state
                    new_state = vals['state']

                    if not (current_state == 'in_progress' and new_state == 'completed'):
                        raise AccessError("You can only change state from In Progress to Completed.")

        return super(Task, self).write(vals)


    @api.constrains('task_line_ids', 'estimated_time')
    def check_total_time(self):
        total_time = sum(line.duration for line in self.task_line_ids)
        if total_time > self.estimated_time:
            raise ValidationError("Total time spent exceeds estimated time for this task.")

    def set_state_closed(self):
        for task in self:
            task.state = 'closed'

    def check_is_late_tasks(self):
        task_ids = self.search(['|', ('state', '=', 'new'), ('state', '=', 'in_progress')])
        for task in task_ids:
            task.is_late = task.due_date < fields.Date.today()

    @api.depends('task_line_ids.duration')
    def _compute_total_time(self):
        for task in self:
            task.total_time = sum(line.duration for line in task.task_line_ids)

    def multi_assign_tasks(self):
        for task in self:
            if task.state not in ['new', 'in_progress']:
                raise ValidationError("Only tasks in 'New' or 'In Progress' state can be assigned.")
        action = self.env['ir.actions.actions']._for_xml_id('todo_management.multi_assign_wizard_action')
        action['context'] = {
            'default_task_ids': self.ids,
        }
        return action

class TaskLine(models.Model):
    _name = 'todo.task.line'

    task_id = fields.Many2one('todo.tasks')
    date = fields.Date()
    description = fields.Text()
    duration = fields.Integer('Time Spent (hours)')
