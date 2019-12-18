# -*- coding: utf-8 -*-
{
    'name': "vit invoice bill",

    'summary': """
        Add Unit
        Add Lokasi - Bisnis
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "asopkarawang@gmail.com",
    'website': "http://www.vitraining.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/bill.xml',
        'views/tax.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}