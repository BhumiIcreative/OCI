{
    'name': 'Artemis Checklists',
    'version': '18.0.1.0.0',
    'summary': ' ',
    'description': """ """,
    'category': 'Field Service',
    "author": "Aktiv software / Groupe OCI",
    "website": "https://www.aktivsoftware.com / https://www.oci.fr",
    'license': 'LGPL-3',
    'depends': ['industry_fsm'],
    'data': [
        "data/checklist_data.xml",
        "security/ir.model.access.csv",
        "views/checklist_views.xml",
        "views/res_config_settings_views.xml",
        "views/project_task_views.xml",


    ],
    'installable': True,
    'application': False,
    'auto_install': False,

}
