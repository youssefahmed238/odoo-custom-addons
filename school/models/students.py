from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Students(models.Model):
    _name = 'students'

    student_code = fields.Integer(required=1)
    name = fields.Char(required=1)
    age = fields.Integer(default=15)
    class_id = fields.Many2one('classes', string='Class', required=True)

    _sql_constraints = [
        ('code_unique', 'unique("student_code")', 'student code already exists!'),
    ]

    @api.constrains('student_code')
    def _check_code(self):
        for rec in self:
            try:
                code = int(rec.student_code)
                if code <= 0:
                    raise ValidationError("Code must be a positive number")
            except ValueError:
                raise ValidationError("Code must be a number")

    @api.constrains('age')
    def _check_age(self):
        for rec in self:
            if rec.age <= 4:
                raise ValidationError("Age must be greater than 4")
            if rec.age > 25:
                raise ValidationError("Age cannot be greater than 25")
