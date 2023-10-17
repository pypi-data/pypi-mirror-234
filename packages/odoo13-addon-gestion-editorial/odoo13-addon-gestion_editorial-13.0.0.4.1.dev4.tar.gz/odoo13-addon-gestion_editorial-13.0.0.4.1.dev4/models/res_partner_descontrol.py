from odoo import models, fields

class EditorialPartners(models.Model):
    """ Extend res.partner template for editorial management """

    _description = "Editorial Partners"
    _inherit = 'res.partner'
    # we inherited res.partner model which is Odoo built in model and edited several fields in that model.
    cliente_num = fields.Integer(string="Num. cliente",
                           help="Número interno de cliente")
    is_author = fields.Boolean(string="Es autor", default=False,
                           help="Indica que el contacto es autor")
    tipo_cliente = fields.Selection([('libreria', 'Librería'), ('parada_distri', 'Parada distri'), ('institucional', 'Institucional'), ('otro','Otro')], default='libreria')
