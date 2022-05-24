{
    'name': 'Learn',  #nama modul yg dibaca user di UI
    'version': '1.0',
    'author': 'Felicia',
    'summary': 'Modul Idea SIB UK Petra', #deskripsi singkat dari modul
    'description': 'Learn module', #bisa nampilkan gambar/ deskripsi dalam bentuk html. html diletakkan
    #di idea/static/description, bisa kasi icon modul juga.
    'category': 'Latihan',
    'website': 'http://sib.petra.ac.id',
    'depends': ['base'],  # list of dependencies, conditioning startup order
    'data': [
        # 'Security/ir.model.access.csv',
        # 'views/idea_views.xml',
        # 'views/voting_views.xml',
    ],
    'qweb':[],  #untuk memberi tahu static file, misal CSS
    'demo': [], #demo data (for unit tests)
    'installable': True,
    'auto_install': False,  # indikasi install, saat buat database baru
    'application': True,
    "sequence": -1 # Supaya Tampil Paling Kiri Atas
}