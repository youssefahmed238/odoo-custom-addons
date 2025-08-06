{
    'name': 'School',
    'author': 'Youssef',
    'category': '',
    'version': '17.0.0.1.0',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/school_menu.xml',
        'views/students_view.xml',
        'views/classes_view.xml',
        'views/courses_view.xml',
        'views/high_school_students_view.xml',
        'views/kindergartens_classes_view.xml',
    ],
    'images': [
        'static/description/icon.png'
    ],
    'application': True,
}