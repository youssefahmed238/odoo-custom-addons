from odoo import models, fields

class Classes(models.Model):
    _name = 'classes'

    name = fields.Char(required = 1)
    class_code = fields.Char(required = 1)
    years_of_study = fields.Selection([
        ('first', 'First Year'),
        ('second', 'Second Year'),
        ('third', 'Third Year'),
        ('fourth', 'Fourth Year'),
    ], default = 'first', required = 1)
    student_ids = fields.One2many('students', 'class_id', string='Students')
    course_ids = fields.Many2many('courses', string='Courses')

    _sql_constraints = [
        ('class_code_unique', 'unique("class_code")', 'Class code already exists!'),
    ]
