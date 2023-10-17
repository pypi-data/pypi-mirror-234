from odoo import models, fields

class EditorialPurchaseOrderLine(models.Model):
    """ Extend purchase.order.line template for editorial management """

    _description = "Editorial Purchase Order Line"
    _inherit = 'purchase.order.line' # odoo/addons/purchase/models/purchase.py

    product_barcode = fields.Char(string='Código de barras / ISBN', related='product_id.barcode', readonly=True)
