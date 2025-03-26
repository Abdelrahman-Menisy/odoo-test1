{
    "name": "Real State",
    "summary": "Real State",
    "description": """
        Real State app 
    """,
    "version": "1.0",
    "author": "Menisy",
    "category": "Real State",
    "depends": ["base", 'contacts', 'account'],
    "data": [
        "security/ir.model.access.csv",
        "views/real_state_view.xml",
        "views/invoice_view_inherit.xml",
        ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "sequence": 1,
    "license":"LGPL-3",
    "company": "tecfy",
    "website": "https://www.tecfy.co",
}