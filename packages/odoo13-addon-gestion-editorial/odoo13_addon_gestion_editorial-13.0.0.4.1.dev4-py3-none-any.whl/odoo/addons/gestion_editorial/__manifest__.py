# -*- coding: utf-8 -*-
######################################################################################
#
#         License**
#
########################################################################################
{
    'name': 'Sistema de gestión Editorial',
    'version': '13.0.0.4.0',
    'summary': 'Módulo para gestión de la editorial Descontrol.',
    'description': 'Módulo para gestión de la editorial Descontrol.',
    'category': 'Industries',
    'author': 'Colectivo DEVCONTROL',
    'author_email': 'devcontrol@zici.fr',
    'maintainer': 'Colectivo DEVCONTROL',
    'company': 'Colectivo DEVCONTROL',
    'website': 'https://framagit.org/devcontrol',
    'depends': ['product', 'account', 'sale_stock', 'base', 'account_invoice_pricelist', 'sale_purchase'],
    'data': [
        'wizards/liquidacion_lineas_pendientes/liquidacion_lineas_pendientes.xml',
        'views/product_descontrol_view.xml',
        'views/res_partner_descontrol_view.xml',
        'views/liquidacion_descontrol_view.xml',
        'views/sale_order_descontrol_view.xml',
        'views/purchase_order_descontrol_view.xml',
        'views/stock_picking_descontrol_view.xml',
        'views/stock_quant_descontrol_view.xml',
        'views/report_saleorder_document_descontrol_view.xml',
        'views/product_pricelist_descontrol_view.xml'
    ],
    'images': ['static/description/logo-devcontrol.png'],
    'license': 'OPL-1',
    'price': 0,
    'currency': 'EUR',
    'installable': True,
    'application': False,
    'auto_install': False,
}
