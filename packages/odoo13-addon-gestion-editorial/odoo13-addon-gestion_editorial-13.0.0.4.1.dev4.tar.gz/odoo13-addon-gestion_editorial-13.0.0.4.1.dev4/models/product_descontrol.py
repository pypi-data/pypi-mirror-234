from odoo import models, fields, api, exceptions

class EditorialProducts(models.Model):
    """ Extend product template for editorial management """

    _description = "Editorial Products"
    _inherit = 'product.template'
    # we inherited product.template model which is Odoo/OpenERP built in model and edited several fields in that model.
    isbn_number = fields.Char(string="ISBN", copy=False, required=False,
                              help="International Standard Book Number \
                              (ISBN)")
    purchase_ok = fields.Boolean('Can be Purchased', default=False)
    author_name = fields.Many2many("res.partner", string="Autores", required=False,
                                   help="Nombre del autor", domain="[('is_author','=',True)]")

    @api.constrains('isbn_number')
    def check_is_isbn13(self):
        for record in self:
            if record.isbn_number:
                n = record.isbn_number.replace('-','').replace(' ', '')
                if len(n) != 13:
                    raise exceptions.ValidationError("El ISBN debe tener 13 dígitos")
                product = (sum(int(ch) for ch in n[::2]) + sum(int(ch) * 3 for ch in n[1::2]))
                if product % 10 != 0:
                    raise exceptions.ValidationError("El ISBN %s no es válido." % record.isbn_number)
        # all records passed the test, don't return anything

    # DDAA: Derechos de autoría
    # Cuando se selecciona la categoría "All / Libros" (con id 5), se establecen los valores por defecto:
    # Producto que se puede vender y comprar y es almacenable.
    @api.onchange('categ_id')
    def _onchange_uom(self):
        if self.categ_id:
            if self.categ_id.id == 5:# categoria Libro
                self.sale_ok=True
                self.purchase_ok=True
                self.type='product'
                self.genera_ddaa = True
            elif self.categ_id.id == 11:# categoria Libro Digital
                self.sale_ok=True
                self.purchase_ok=True
                self.type='consu'
                self.genera_ddaa = True

    # DDAA: Derechos de autoría
    # Check one2one relation. Here between "producto_referencia" y "derecho_autoria"
    #
    # Note: we are creating the relationship between the templates.
    # Therefore, when we add the product to a stock.picking or a sale or purchase, we are actually adding the product  and not the template.
    # Please use product_tmpl_id to access the template of a product.
    producto_referencia = fields.One2many("product.template", 'derecho_autoria', domain="[('categ_id','in',[5, 11])]", string="Libro de referencia",
                                   help="Este campo se utiliza para relacionar el derecho de autoría con el libro")

    # prod_ref = fields.Many2one("product.template", compute='compute_autoria', inverse='autoria_inverse', string="prod ref",
    #                             domain="[('categ_id','in',[5, 11])]", required=False)

    derecho_autoria = fields.Many2one("product.template", domain="[('categ_id','=',4)]", string="Producto ddaa",
                                    help="Este campo se utiliza para relacionar el derecho de autoría con el libro")

    receptora_derecho_autoria = fields.Many2many("res.partner", 'receptora_autoria_product_template', 'product_id', 'partner_id',
                                   copy=False,
                                   string="Receptor derechos autoría",
                                   help="Nombre de la receptora de derechos de autoría")

    genera_ddaa = fields.Boolean('Genera derechos de autoría', default=False)

    # @api.depends('producto_referencia')
    # def compute_autoria(self):
    #     if len(self.derecho_autorias) > 0:
    #         self.derecho_autoria = self.derecho_autorias[0]

    # def autoria_inverse(self):
    #     if len(self.derecho_autorias) > 0:
    #         # delete previous reference
    #         ddaa = self.env['product.template'].browse(self.derecho_autorias[0].id)
    #         ddaa.producto_referencia = False
    #     # set new reference
    #     self.derecho_autoria.producto_referencia = self

    # DDAA: Derechos de autoría
    # Se crea un producto asociado con categoría "All / Derechos de autor" (con id 4)
    @api.model_create_multi
    def create(self, vals_list):
        templates = super(EditorialProducts, self).create(vals_list)
        vals = vals_list[0]
        if vals.get('categ_id') in [5, 11] and vals.get('genera_ddaa') == True:
            self.env['product.template'].create({
                'name': 'DDAA de ' + vals.get('name'),
                'categ_id': 4,
                'list_price': vals.get('list_price') * 0.1,
                'type': 'service',
                'sale_ok': False,
                'purchase_ok': True,
                'author_name': vals.get('author_name'),
                'receptora_derecho_autoria': vals.get('author_name'),
                'producto_referencia': [templates.id],
                'derecho_autoria': False
            })
        return templates
