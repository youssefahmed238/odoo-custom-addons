{
    'name': 'Todo',
    'author': 'Youssef',
    'category': '',
    'version': '17.0.0.1.0',
    'depends': ['base', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/todo_management_menu.xml',
        'views/tasks_view.xml',
        'wizard/multi_assign_wizard_view.xml',
        'reports/task_report.xml',
    ],
    'images': [
        'static/description/icon.png',
    ],
    'application': True,

}
