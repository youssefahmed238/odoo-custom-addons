from odoo import models, fields

class Courses(models.Model):
    _name = 'courses'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Course'

    name = fields.Char(required = 1, string = 'Course Name', tracking = 1)
    course_code = fields.Char(required = 1, tracking = 1)
    class_ids = fields.Many2many('classes', string='Classes', tracking = 1)
    description = fields.Text(tracking = 1)

    _sql_constraints = [
        ('name_unique', 'unique("name")', 'Course name already exists!'),
        ('course_code_unique', 'unique("course_code")', 'Course code already exists!'),
    ]