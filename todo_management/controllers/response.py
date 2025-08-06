from odoo import http
from odoo.http import request


def response(message=None, pagination_info=None, data=None, status=200):
    payload = {}

    if message:
        payload['message'] = message

    if data:
        payload['data'] = data

    if pagination_info:
        payload['pagination_info'] = pagination_info

    return request.make_json_response(payload, status=status)
