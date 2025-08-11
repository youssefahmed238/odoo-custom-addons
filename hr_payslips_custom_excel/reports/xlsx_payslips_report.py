from odoo import http
from odoo.http import request
from ast import literal_eval
import io
import xlsxwriter


class XlsxPayslipsReport(http.Controller):

    @http.route('/payslips/excel/report/<string:payslip_ids>', type='http', auth='user')
    def download_payslips_excel_report(self, payslip_ids):

        payslips = request.env['hr.payslip'].browse(literal_eval(payslip_ids) if payslip_ids else [])

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        worksheet = workbook.add_worksheet('Payslips')

        header_format = workbook.add_format({
            "bg_color": "#b3c7e6",
            'bold': True,
            'border': 1,
            "align": "center"
        })

        field_format = workbook.add_format({
            'border': 1,
            'align': 'center',
        })

        headers = ['Code', 'Name', "Nationality", "From", "To", "Basic Salary", "Additional Salary",
                   "Housing Allowance", "Transportation Allowance", "Total Deducted", "Gross Salary", "Net Salary",
                   "Note"]

        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, header_format)

        row = 1
        for slip in payslips:
            worksheet.write(row, 0, slip.employee_id.id or '', field_format)
            worksheet.write(row, 1, slip.employee_id.name or '', field_format)
            worksheet.write(row, 2, slip.employee_id.country_id.name or '', field_format)
            worksheet.write(row, 3, str(slip.date_from) if slip.date_from else '', field_format)
            worksheet.write(row, 4, str(slip.date_to) if slip.date_to else '', field_format)

            def get_line_total(code):
                total = sum(line.total for line in slip.line_ids if line.code == code)
                return total or 0.0

            worksheet.write(row, 5, get_line_total('BASIC'), field_format)

            allowance_codes = ['HRA', 'CA', 'CAGG', 'MA']
            additional_salary = sum(get_line_total(code) for code in allowance_codes)

            worksheet.write(row, 6, additional_salary, field_format)
            worksheet.write(row, 7, get_line_total('HRA'), field_format)
            worksheet.write(row, 8, get_line_total('CA'), field_format)

            total_deducted = sum(get_line_total(code) for code in ['PF', 'PT']) * -1

            worksheet.write(row, 9, total_deducted, field_format)
            worksheet.write(row, 10, get_line_total('GROSS'), field_format)
            worksheet.write(row, 11, get_line_total('NET'), field_format)
            worksheet.write(row, 12, slip.note or '', field_format)

            row += 1

        workbook.close()
        output.seek(0)

        file_name = 'payslips_report.xlsx'

        return request.make_response(
            output.getvalue(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', f'attachment; filename={file_name}'),
            ]
        )
