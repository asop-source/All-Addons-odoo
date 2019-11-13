{
	"name": "Insfratucture Monitoring System",
	"version": "1.0", 
	"depends": [
		"base",
		"hr",
	],
	"author": "asopkarawang@gmail.com", 
	"category": "Monitoring System", 
	'website': 'http://www.vitraining.com',
	"description": """\
Data Centre Insfraructure Monitoring System

""",
	"data": [
		"view/menu.xml",
		"view/data/perangkat_dc.xml",
		"view/data/maintenance.xml",
		"view/data/distribution.xml",
		"view/data/landistribution.xml",
		"view/data/utilitas.xml",
		"view/data/recruitment_doc.xml",
		"view/data/sop_doc.xml",
		"view/data/bcp_doc.xml",
		"view/data/berita_doc.xml",
		"view/data/agenda_doc.xml",
		"view/data/capacity.xml",


		"view/master/cpu.xml",
		"view/master/disk.xml",
		"view/master/fungsi.xml",
		"view/master/kelamin.xml",
		"view/master/koneksi.xml",
		"view/master/location.xml",
		"view/master/merk.xml",
		"view/master/pendidikan.xml",
		"view/master/posisi.xml",
		"view/master/publish.xml",
		"view/master/ram.xml",
		"view/master/ruang.xml",
		"view/master/spesifikasi.xml",

		# "layout.xml",
	],
	"installable": True,
	"auto_install": False,
    "application": True,
}
