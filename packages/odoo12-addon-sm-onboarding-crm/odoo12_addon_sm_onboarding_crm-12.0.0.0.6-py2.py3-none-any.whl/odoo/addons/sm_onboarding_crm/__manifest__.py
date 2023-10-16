{
    'name': "sm_onboarding_crm",

    'summary': """
    onboarding customers and company employees with crm.lead""",

    'description': """
    onboarding customers and company employees with crm.lead""",

    'author': "Som Mobilitat",
    'website': "https://git.coopdevs.org/coopdevs/odoo/odoo-addons/vertical-carsharing",

    'category': 'vertical-cooperative',
    'version': '12.0.0.0.6',

    'depends': ['base', 'vertical_carsharing', 'crm', 'crm_metadata', 'crm_metadata_rest_api'],

    'data': [
        "data/crm_team_data.xml",
        "data/utm_source_data.xml",
        "views/utm.xml",
        "views/crm_lead_views.xml",
    ],

    'demo': [
    ],
    'application': True,
}
