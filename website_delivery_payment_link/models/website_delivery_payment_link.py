from odoo import models, fields


class DeliveryPaymentLink(models.Model):
    _inherit = 'delivery.carrier'

    payment_method_id = fields.Many2one('payment.method')
