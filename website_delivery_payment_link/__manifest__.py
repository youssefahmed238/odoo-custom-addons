{
    'name': 'Link Payment and Shipping Methods in Website',
    'author': 'Youssef',
    'category': 'Website',
    'version': '17.0.1.0.0',
    'depends': ['website_sale'],
    'data': [
        'views/delivery_carrier_view.xml',
        'views/payment_method_view.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_delivery_payment_link/static/src/js/linkDeliveryWithPayment.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': True,
}
