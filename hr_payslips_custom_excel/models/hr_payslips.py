from odoo import models, fields, api


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def action_export_payslips_excel(self):
        return {
            'type': 'ir.actions.act_url',
            'url': f'/payslips/excel/report/{self.ids or self.env.context.get("active_ids")}',
            'target': 'new',
        }
