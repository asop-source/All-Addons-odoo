# -*- coding: utf-8 -*-
{
    'name': "Vit Purchase Request",

    'summary': """
        Rename Product Request = Purchase Request

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
    'depends': ['base','vit_product_request','vit_product_request_analytic'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/location_business.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}