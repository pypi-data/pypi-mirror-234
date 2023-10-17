from odoo import models, fields, api

class EditorialSaleOrder(models.Model):
    """ Extend sale.order template for editorial management """

    _description = "Editorial Sale Order"
    _inherit = 'sale.order' # odoo/addons/sale/models/sale.py

    @api.onchange('order_line')
    def default_pricelist_when_order_line(self):
        if self.order_line:
            if self.pricelist_id.route_id:
                for line in self.order_line:
                    line.route_id = self.pricelist_id.route_id.id

    @api.onchange('pricelist_id')
    def default_pricelist_when_pricelist_id(self):
        if self.order_line:
            if self.pricelist_id.route_id:
                for line in self.order_line:
                    line.route_id = self.pricelist_id.route_id.id
                    line.price_unit = line._get_display_price(line.product_id)

class EditorialSaleOrderLine(models.Model):
    """ Extend sale.order.line template for editorial management """
    _description = "Editorial Sale Order Line"
    _inherit = 'sale.order.line' # odoo/addons/sale/models/sale.py

    product_barcode = fields.Char(string='Código de barras / ISBN', related='product_id.barcode', readonly=True)
    product_list_price = fields.Float(string='PVP', related='product_id.list_price', readonly=True)
