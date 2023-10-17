{
    'name': "document_validation_dms_field",
    'version': '12.0.0.0.1',
    'depends': ['base', 'crm', 'dms', 'dms_field'],
    'author': "Som IT, Som Connexió",
    'category': 'Document Validation dms field',
    'summary': "",
    'data': [
        'security/ir.model.access.csv',
        'data/dms_category_data.xml',
        'data/dms_storage_data.xml',
        'views/crm_dms_rules_views.xml',
        'views/dms_category_views.xml',
        'views/dms_directory_views.xml',
        'views/dms_field_views.xml',
        'views/crm_lead_views.xml',
        'views/crm_views.xml',
    ],
}
