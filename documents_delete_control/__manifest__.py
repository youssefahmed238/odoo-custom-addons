{
    'name': 'Documents Delete Control',
    'author': 'Youssef',
    'category': 'Productivity',
    'version': '17.0.0.1.0',
    'depends': ['documents'],
    'data': [
        'security/security.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'documents_delete_control/static/src/js/documents_inspector_inherit.js',
            'documents_delete_control/static/src/xml/documents_inspector_inherit.xml',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': True,
}
