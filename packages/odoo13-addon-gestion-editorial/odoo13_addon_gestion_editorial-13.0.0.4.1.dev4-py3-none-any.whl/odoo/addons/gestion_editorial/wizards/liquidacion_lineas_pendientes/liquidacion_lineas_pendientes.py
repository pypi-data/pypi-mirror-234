from odoo import api, fields, models, exceptions

import logging
_logger = logging.getLogger(__name__)



class LiquidacionWizard(models.TransientModel):
    """ Wizard: Ayuda para seleccionar las stock.move.lines pendientes de liquidar """
    _name = 'liquidacion.wizard.descontrol'
    _description =  "Wizard Depósito"

    partner_id = fields.Many2one('res.partner', string='Cliente')

    liquidacion_line_ids = fields.One2many('liquidacion.line.descontrol', 'liquidacion_wizard_id', string="Lineas de Liquidacion", copy=True)

    @api.onchange('partner_id')
    def _update_invoice_lines(self):
        for wizard in self:
            domain = [
                ('owner_id', '=', self.env.context.get('partner_id')),
                ('location_id', '=' , 17), # This is the id of the Location DS/Depósitos (the source of the move)
                ('location_dest_id', '=' , 5), # This is the id of the Location Partner Locations/Customers (the destination of the move)
                ('state', 'in', ('assigned', 'partially_available')),
            ]
            pendientes_liquidar_line_ids = self.env['stock.move.line'].search(domain)
            wizard.liquidacion_line_ids = None
            for move_line in pendientes_liquidar_line_ids:
                wizard._update_liquidacion_line(move_line)

    def _update_liquidacion_line(self, move_line):
        liquidacion_line_aux = self.liquidacion_line_ids.filtered(lambda line: line.product_id == move_line.product_id)
        if len(liquidacion_line_aux) <= 0:
            liquidacion_line = self.env['liquidacion.line.descontrol'].create({'liquidacion_wizard_id': self.id, 'product_id': move_line.product_id.id})
        else:
            liquidacion_line = liquidacion_line_aux[0]
        total_product_uom_qty = liquidacion_line.total_product_uom_qty + move_line.product_uom_qty
        liquidacion_line.update({'total_product_uom_qty': total_product_uom_qty})
        liquidacion_line.total_qty_done += move_line.qty_done
        return liquidacion_line

    @api.onchange('liquidacion_line_ids')
    def _check_liquidacion_lines(self):
        for wizard in self:
            for liquidacion_line in wizard.liquidacion_line_ids:
                if liquidacion_line.total_qty_a_liquidar and liquidacion_line.total_qty_a_liquidar > 0.0:
                    value = liquidacion_line.total_product_uom_qty - liquidacion_line.total_qty_done
                    if liquidacion_line.total_qty_a_liquidar > liquidacion_line.total_product_uom_qty - liquidacion_line.total_qty_done:
                        raise exceptions.ValidationError("La cantidad a liquidar no puede ser mayor que la diferencia entre el total en depósito y el total hecho.")

    @api.model
    def default_get(self, fields):
        res = super(LiquidacionWizard, self).default_get(fields)
        res['partner_id'] = self.env.context.get('partner_id')
        return res

    def seleccionar_para_liquidar(self):
        # self.ensure_one()
        liquidacion = self.env['account.move'].browse(self.env.context.get('liquidacion_id'))
        for liquidacion_line in self.liquidacion_line_ids:
            if liquidacion_line.total_qty_a_liquidar > 0.0:
                _logger.debug("***************************************************** seleccionar_para_liquidar ")

                # TODO esto sólo funcionaría para las tarifas con una línea (item_ids[0]):
                price_unit = liquidacion.pricelist_id.get_product_price(
                    liquidacion_line.product_id, 1, self.partner_id
                )
                quantity = liquidacion_line.total_qty_a_liquidar
                product = liquidacion_line.product_id
                partner = self.partner_id.id

                vals = {
                    'name': liquidacion_line.product_id.name,
                    'move_id': self.env.context.get('liquidacion_id'),
                    'partner_id': partner,
                    'product_id': product.id,
                    'journal_id': liquidacion.journal_id,
                    'quantity': quantity,
                    'price_unit': price_unit,
                    'tax_ids': product.taxes_id,
                }
                liquidacion.write({'invoice_line_ids': [(0,0,vals)]}) # = self.env['account.move.line'].new(vals)
        liquidacion._move_autocomplete_invoice_lines_values()
        liquidacion._recompute_payment_terms_lines()
        return {'type': 'ir.actions.act_window_close'}

class EditorialLiquidacionLine(models.TransientModel):
    """ Modelo de línea de liquidación"""
    _name = "liquidacion.line.descontrol"
    _description = "Linea Liquidacion Descontrol"

    # company_id = fields.Many2one(related='liquidacion_id.company_id', store=True, readonly=True)
    liquidacion_wizard_id = fields.Many2one('liquidacion.wizard.descontrol', "Liquidacion Wizard", index=True, ondelete="cascade")
    product_id = fields.Many2one('product.product', 'Producto')
    product_barcode = fields.Char('Código de barras / ISBN', related='product_id.barcode', store=True, readonly=True)
    product_name = fields.Char('Nombre', related='product_id.name', store=True, readonly=True)
    total_product_uom_qty = fields.Float('Total en Depósito', default=0.0, digits='Product Unit of Measure', required=True, copy=False)
    total_qty_done = fields.Float('Total Hecho', default=0.0, digits='Product Unit of Measure', copy=False)
    total_qty_disponibles = fields.Float('Total en depósito', default=0.0, digits='Product Unit of Measure', copy=False, compute="_compute_available")
    total_qty_a_liquidar = fields.Float('A Liquidar', default=0.0, digits='Product Unit of Measure', copy=False)

    @api.depends('total_qty_done', 'total_product_uom_qty')
    def _compute_available(self):
        for record in self:
            record.total_qty_disponibles = record.total_product_uom_qty - record.total_qty_done
