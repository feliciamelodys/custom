# -*- coding: utf-8 -*-
{
    'name': "smk-telkom",

    'summary': """
        Reynald Silva B""",

    'description': """
        latihan
    """,

    'author': "Reynald S",
    'website': "http://www.instagram.com/reysilvaa12",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/buku.xml',
        'views/pengarang.xml',
        'views/categori.xml',
        'views/lokasi.xml',
        'views/anggota.xml',
        'views/wilayah.xml',
        'views/peminjaman.xml',
        # 'security/security.xml',


    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
