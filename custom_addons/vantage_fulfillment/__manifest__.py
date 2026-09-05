{
    'name': 'VantageOps Fulfillment (Operational Execution)',
    
    'category': 'Inventory/Delivery',
    'summary': 'Multi-Warehouse Auto-Split & Live Upsell Engine (Ashrith)',
    'author': 'Ashrith',
    'depends': ['vantage_core', 'sale_stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/fulfillment_views.xml',
    ],
    'installable': True,
    'application': False,
}
