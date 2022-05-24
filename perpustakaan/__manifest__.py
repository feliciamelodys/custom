{
    'name': 'Perpustakaan',  #nama modul yg dibaca user di UI
    'version': '1.0',
    'author': 'Felicia',
    'summary': 'Modul untuk simulasi perpustakaan', #deskripsi singkat dari modul
    'description': 'UTS Konfigurasi ERP - C14190089', #bisa nampilkan gambar/ deskripsi dalam bentuk html. html diletakkan
    #di idea/static/description, bisa kasi icon modul juga.
    'category': 'Latihan',
    'website': 'http://sib.petra.ac.id',
    'depends': ['account'],  # list of dependencies, conditioning startup order
    'data': [
        'data/res_groups_data.xml',
        'data/sequence.xml',
        'security/ir.model.access.csv',
        'views/buku_views.xml',
        'views/kategori_views.xml',
        'views/res_partner_views.xml',
        'views/kartu_perpustakaan_views.xml',
        'views/menu.xml',
    ],
    'qweb':[],  #untuk memberi tahu static file, misal CSS
    'demo': [], #demo data (for unit tests)
    'installable': True,
    'auto_install': False,  # indikasi install, saat buat database baru
    'application': True
}