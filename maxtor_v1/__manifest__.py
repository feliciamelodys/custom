{
    'name': 'Maxtor',  #nama modul yg dibaca user di UI
    'version': '1.0',
    'author': 'Felicia',
    'summary': 'Modul untuk perusahaan Maxtor', #deskripsi singkat dari modul
    'description': 'UAS Konfigurasi ERP - C14190089', #bisa nampilkan gambar/ deskripsi dalam bentuk html. html diletakkan
    #di idea/static/description, bisa kasi icon modul juga.
    'category': 'Latihan',
    'website': 'http://sib.petra.ac.id',
    'depends': ['account','stock','muk_web_theme'],  # list of dependencies, conditioning startup order
    'data': [
        'data/res_groups_data.xml',
        'data/sequence.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/merk_views.xml',
        'views/nama_barang_views.xml',
        'views/product_views.xml',
        'views/res_partner_views.xml',
        'views/nota_penjualan_views.xml',
        'views/retur_views.xml',
        'reports/penjualan_report.xml',
        'views/menu.xml',
    ],
    'qweb':[],  #untuk memberi tahu static file, misal CSS
    'demo': [], #demo data (for unit tests)
    'installable': True,
    'auto_install': False,  # indikasi install, saat buat database baru
    'application': True
}