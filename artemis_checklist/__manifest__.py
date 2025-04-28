{
    'name': 'Artemis Checklists',
    'version': '18.0.1.0.0',
    'summary': ' ',
    'description': """ """,
    'category': 'Field Service',
    "author": "Aktiv software / Groupe OCI",
    "website": "https://www.aktivsoftware.com / https://www.oci.fr",
    'license': 'LGPL-3',
    'depends': ['industry_fsm', 'project'],
    'data': [
        "data/checklist_data.xml",
        "data/report_paperformate_data.xml",
        "security/ir.model.access.csv",
        "report/checklist_report.xml",
        "report/sav_intervention_template.xml",
        "report/intervention_training_template.xml",
        "report/fire_detection_template.xml",
        "report/intervention_preventive_template.xml",
        "views/checklist_views.xml",
        "views/res_config_settings_views.xml",
        "views/project_task_views.xml",
        "views/res_partner_views.xml",
    ],
    "assets": {
        "web.report_assets_common": [
            "/artemis_checklist/static/src/scss/report_style.scss",
        ],
        'web.assets_backend': [
            'artemis_checklist/static/src/**',

        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
