# -*- coding: utf-8 -*-
{
    'name': "vit quotation",

    'summary': """
        Add Unit
        Add Lokasi - Bisnis
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "asopkarawang@gamil.com",
    'website': "http://www.vitraining.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','account','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views.xml',
        'menu.xml'
    ],
}