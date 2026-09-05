{
    'name': 'VantageOps Governance (Commercial Control)',
    'version': '17.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Approval Routing, Chatter Escalations & Portal Negotiation (Akthar)',
    'author': 'Akthar',
    'depends': ['vantage_core', 'portal', 'mail'],
    'data': [
        'views/governance_views.xml',
        'views/portal_templates.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'installable': True,
    'application': False,
}
