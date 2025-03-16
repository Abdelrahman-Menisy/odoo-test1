{
    'name': 'Owl Reload Button (sales)',
    'version': '1.0',
    'summary': 'Owl Reload Button',
    'description': """
        Owl Reload Button in sales view
    """,
    'category': 'Owl',
    'author': 'menisy',
    'depends': ['web'],
    'data': [
        # 'views/assets.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'owl_reload_button/static/src/js/add_reload_button.js',
            'owl_reload_button/static/src/xml/add_reload_button.xml',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
    
}