{
    'name': 'Owl Kanban Another Way',
    'summary': 'Owl Kanban Another Way',
    'description': 'Owl Kanban Another Way',
    'author': 'Menisy',
    'category': 'Owl',
    'version': '1.0',
    'depends': ['web','contacts','sale'],
    'data': [
        'views/res_partner.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'owl_kanban_another_way/static/src/js/*.js',
            'owl_kanban_another_way/static/src/xml/*.xml',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
}