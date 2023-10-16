{
    'name': "sm_donation_crm",

    'summary': """Manage donation in crm.lead""",

    'description': """Manage donation in crm.lead""",

    'author': "Som Mobilitat",
    'website': "https://git.coopdevs.org/coopdevs/odoo/odoo-addons/vertical-carsharing",

    'category': 'vertical-cooperative',
    'version': '12.0.0.0.6',

    'depends': ['base', 'vertical_carsharing', 'crm', 'crm_metadata', 'crm_metadata_rest_api'],

    'data': [
        'data/utm_source_data.xml',
        'data/crm_team_data.xml',
        'data/crm_stage_data.xml',
        'views/crm_lead_views.xml',
    ],

    'demo': [

    ],
    'application': True,
}
