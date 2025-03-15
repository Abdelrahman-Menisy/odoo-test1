{
    'name': 'Owl Kanban View',
    'version': '1.0',
    'summary': 'Owl Kanban View',
    'description': """
        Owl Kanban View
    """,
    'category': 'Owl',
    'author': 'menisy',
    'depends': ['web'],
    'data': [
        # 'views/assets.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'owl_kanban_view/static/src/js/owl_kanban_view.js',
            'owl_kanban_view/static/src/xml/owl_kanban_view.xml',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
    
}