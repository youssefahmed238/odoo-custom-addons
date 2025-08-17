from odoo import http
from odoo.http import request


class DeliveryPaymentLinkController(http.Controller):

    @http.route('/delivery_payment/map', type='json', auth='public', website=True)
    def delivery_payment_map(self):

        delivery_carrier = request.env['delivery.carrier'].sudo().search([])
        payment_methods = request.env['payment.method'].sudo().search([])

        delivery_payment_map = {}
        payment_delivery_map = {}

        for delivery in delivery_carrier:
            delivery_payment_map[str(delivery.id)] = str(delivery.payment_method_id.id or '')

        for payment in payment_methods:
            payment_delivery_map[str(payment.id)] = str(payment.delivery_carrier_id.id or '')

        return {
            'delivery_payment_map': delivery_payment_map,
            'payment_delivery_map': payment_delivery_map,
        }
