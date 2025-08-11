from odoo import models, fields, api

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def action_export_payslips_excel(self):
        print("Exporting payslips to Excel...")