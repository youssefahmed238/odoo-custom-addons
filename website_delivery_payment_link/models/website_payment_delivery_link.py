from odoo import models, fields


class PaymentDeliveryLink(models.Model):
    _inherit = 'payment.method'

    delivery_carrier_id = fields.Many2one('delivery.carrier', string='Delivery Method')
