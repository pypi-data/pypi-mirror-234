from odoo import models, fields, api, _
from odoo.exceptions import UserError

class EditorialPicking(models.Model):
    """ Extend stock.picking template for editorial management """

    _description = "Editorial Stock Picking"
    _inherit = 'stock.picking' # odoo/addons/stock/models/stock_picking.py

    @api.depends('state', 'move_lines', 'move_lines.state', 'move_lines.package_level_id', 'move_lines.move_line_ids.package_level_id')
    def _compute_move_without_package(self):
        for picking in self:
            for move in self.move_lines:
                for ml in move.move_line_ids:
                    ml.owner_id = self.partner_id
            picking.move_ids_without_package = picking._get_move_ids_without_package()

    # DDAA: Derechos de autoría
    # Cuando se valida un stock.picking, se comprueba que la Localización de destino es Partner Locations (con id 5),
    # para hacer la compra de derechos de autoría.
    # También se ha de comprobar cuando se hace un movimiento con origen Partner Locations (que representa una devolución).
    def generar_derechos_autoria(self):
        if self.location_dest_id.id == 5 or self.location_id.id == 5: # This is the id of the Location Partner Locations/Customers
            # Para las líneas que contengan un libro que tenga derechos de autoría
            # Busca una purchase order a ese autor con la línea con el derecho de autoría, si no, créala
            libros = self.move_line_ids_without_package.filtered(lambda line: line.product_id.categ_id.id in [5, 11])
            if libros:
                for libro in libros:
                    # nos aseguramos que el libro genera ddaa
                    if libro.product_id.product_tmpl_id.genera_ddaa == False:
                        continue
                    # nos aseguramos que el llibre.template no tiene ddaa ya
                    ddaa = libro.product_id.product_tmpl_id.derecho_autoria
                    if not ddaa:
                        author = libro.product_id.product_tmpl_id.author_name
                        if not author:
                            continue
                        else:
                            ddaa = self.env['product.template'].create({
                                'name': 'DDAA de ' + libro.product_id.product_tmpl_id.name,
                                'categ_id': 4,
                                'list_price': libro.product_id.product_tmpl_id.list_price * 0.1,
                                'type': 'service',
                                'sale_ok': False,
                                'purchase_ok': True,
                                'author_name': author,
                                'receptora_derecho_autoria': author,
                                'producto_referencia': [libro.product_id.product_tmpl_id.id],
                                'derecho_autoria': False
                            })
                    # en el cas que ja existisquen drets d'autoria, utilitzem el camp receptora_derecho_autoria
                    if not ddaa.receptora_derecho_autoria:
                        continue
                    domain = [
                        ('partner_id', '=', ddaa.receptora_derecho_autoria.id),
                        ('state', '=', 'draft'),
                        ('partner_ref', '=', 'DDAA')
                    ]
                    compra_derechos_autoria = self.env['purchase.order'].search(domain, order='date_order desc')
                    if not compra_derechos_autoria:
                        # crear sale.order a la receptora de derechos
                        compra_derechos_autoria = self.env['purchase.order'].create({
                            'partner_id': ddaa.receptora_derecho_autoria.id,
                            'partner_ref': 'DDAA'
                        })
                    elif len(compra_derechos_autoria) > 1:
                        compra_derechos_autoria = compra_derechos_autoria[0]
                    # buscar línea y sumar (o restar) cantidad
                    linea_libro_compra = compra_derechos_autoria.order_line.filtered(lambda line: line.product_id.product_tmpl_id.id == ddaa.id)
                    # la cantidad a sumar (o restar) de ddaa:
                    cantidad_ddaa = libro.qty_done if self.location_dest_id.id == 5 else 0 - libro.qty_done
                    if linea_libro_compra:
                        if len(linea_libro_compra) > 1:
                            linea_libro_compra = linea_libro_compra[0]
                        linea_libro_compra.write({'product_qty': linea_libro_compra.product_qty + cantidad_ddaa})
                    else:
                        product_id = self.env['product.product'].search([('product_tmpl_id', '=', ddaa.id)])
                        vals = {
                            'name': ddaa.name,
                            'order_id': compra_derechos_autoria.id,
                            'product_id': product_id.id,
                            'product_qty': cantidad_ddaa,
                            'price_unit': ddaa.list_price,
                            'product_uom': 1,
                            'date_planned': compra_derechos_autoria.date_order,
                            'display_type': False
                        }
                        compra_derechos_autoria.write({'order_line': [(0,0,vals)]})

    def button_validate(self):
        self.generar_derechos_autoria()
        return super(EditorialPicking, self).button_validate()


class EditorialStockMoveLine(models.Model):
    """ Extend stock.move.line for editorial management """

    _description = "Editorial Stock Move Line"
    _inherit = 'stock.move.line' # https://github.com/OCA/OCB/blob/13.0/addons/stock/models/stock_move_line.py

    product_barcode = fields.Char(string='Código de barras / ISBN', related='product_id.barcode', readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('location_id') == 8:
                vals['qty_done'] = vals.get('product_uom_qty')
        return super(EditorialStockMoveLine, self).create(vals_list)

class EditorialStockMove(models.Model):
    """ Extend stock.move template for editorial management """

    _description = "Editorial Stock Move"
    _inherit = 'stock.move' # odoo/addons/stock/wizard/stock_move.py

    product_barcode = fields.Char(string='Código de barras / ISBN', related='product_id.barcode', readonly=True)

class EditorialStockImmediateTransfer(models.TransientModel):

    """ Extend stock.immediate.transfer for editorial management """

    _description = "Editorial Stock Immediate Transfer"
    _inherit = 'stock.immediate.transfer' # odoo/addons/stock/models/stock_immediate_transfer.py

    def process(self):
        pick_to_backorder = self.env['stock.picking']
        pick_to_do = self.env['stock.picking']
        for picking in self.pick_ids:
            # If still in draft => confirm and assign
            if picking.state == 'draft':
                picking.action_confirm()
                if picking.state != 'assigned':
                    picking.action_assign()
                    if picking.state != 'assigned':
                        raise UserError(_("Could not reserve all requested products. Please use the \'Mark as Todo\' button to handle the reservation manually."))
                    
            for move in picking.move_lines.filtered(lambda m: m.state not in ['done', 'cancel']):
                for move_line in move.move_line_ids:
                    move_line.qty_done = move_line.product_uom_qty
            if picking._check_backorder():
                pick_to_backorder |= picking
                continue
            pick_to_do |= picking
            
        # Process every picking that do not require a backorder, then return a single backorder wizard for every other ones.
        if pick_to_do:
            pick_to_do.generar_derechos_autoria()
            pick_to_do.action_done()
        if pick_to_backorder:
            return pick_to_backorder.action_generate_backorder_wizard()
        return False