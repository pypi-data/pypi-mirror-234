from odoo import models, fields

class EditorialProductPricelist(models.Model):
    """ Extend product pricelist model for editorial management """

    _description = "Editorial Product Pricelist"
    _inherit = 'product.pricelist'

    route_id = fields.Many2one('stock.location.route', string='Ruta')
