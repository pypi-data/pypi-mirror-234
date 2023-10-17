from odoo import models, fields, api, exceptions
from odoo.tools.float_utils import float_compare

import logging
_logger = logging.getLogger(__name__)


class EditorialLiquidacion(models.Model):
    """ Modelo de liquidación que extiende de account.move """

    # https://github.com/OCA/OCB/blob/13.0/addons/account/models/account_move.py
    _description = "Liquidacion Descontrol"
    _inherit = ['account.move']

    @api.model
    def _get_default_is_liquidacion(self):
        if self._context.get('invoice_type') and self._context['invoice_type'] == 'LIQ':
            return True
        else:
            return False

    is_liquidacion = fields.Boolean(
        "Es liquidacion", default=_get_default_is_liquidacion
    )

    @api.model
    def get_default_journal_depositos(self):
        """ Get the default journal.
        Extend the original function by selecting the journal id with code='LIQ'
        """
        if (
            self._context.get('invoice_type')
            and self._context['invoice_type'] == 'LIQ'
            and self._context.get('default_type')
            and self._context['default_type'] == 'out_refund'
        ):
            journal_liquidacion = self.env['account.journal'].search(
                [('code', '=', 'LIQ')]
            )
            return journal_liquidacion[0]
        else:
            return super(EditorialLiquidacion, self)._get_default_journal()

    journal_id = fields.Many2one(
        'account.journal',
        string='Journal',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        check_company=True,
        domain="[('id', 'in', suitable_journal_ids)]",
        default=get_default_journal_depositos,
    )

    def checkLiquidacionIsValid(self, liquidacion):
        products_to_check = []
        domain = [
            ('owner_id', '=', liquidacion.partner_id.id),
            (
                'location_id',
                '=',
                17,
            ),  # This is the id of the Location DS/Depósitos (the source of the move)
            (
                'location_dest_id',
                '=',
                5,
            ),  # This is the id of the Location Partner Locations/Customers (the destination of the move)
            ('state', 'in', ('assigned', 'partially_available')),
        ]
        pendientes_liquidar_line_ids = self.env['stock.move.line'].search(
            domain, order='date asc'
        )
        for invoice_line in liquidacion.invoice_line_ids:
            invoice_line_qty = invoice_line.quantity
            pendientes_cerrar_stock_lines = pendientes_liquidar_line_ids.filtered(
                lambda pendientes_liquidar_line: pendientes_liquidar_line.product_id
                == invoice_line.product_id
            )
            if (
                not pendientes_cerrar_stock_lines
                or len(pendientes_cerrar_stock_lines) <= 0
            ):
                products_to_check.append((invoice_line.name, 0))
            else:
                sum_available = sum(
                    p.product_uom_qty - p.qty_done
                    for p in pendientes_cerrar_stock_lines
                )
                if sum_available < invoice_line_qty:
                    products_to_check.append((invoice_line.name, sum_available))
        return products_to_check

    def post_y_liquidar(self):
        if not self.is_liquidacion:
            raise exceptions.ValidationError(
                "Sólo se puede liquidar desde una factura tipo liquidación"
            )
        products_to_check = self.checkLiquidacionIsValid(self)
        if len(products_to_check) > 0:
            msg = "No hay stock suficiente disponible en depósito con estos valores. Estos son valores disponibles en depósito:"
            for product in products_to_check:
                msg += "\n* " + str(product[0]) + ": " + str(product[1])
            raise exceptions.UserError(msg)
        domain = [
            ('owner_id', '=', self.partner_id.id),
            (
                'location_id',
                '=',
                17,
            ),  # This is the id of the Location DS/Depósitos (the source of the move)
            (
                'location_dest_id',
                '=',
                5,
            ),  # This is the id of the Location Partner Locations/Customers (the destination of the move)
            ('state', 'in', ('assigned', 'partially_available')),
        ]
        pendientes_liquidar_line_ids = self.env['stock.move.line'].search(
            domain, order='date asc'
        )  # deposito de este contacto
        pickings_to_validate = set()
        for invoice_line in self.invoice_line_ids:
            invoice_line_qty = invoice_line.quantity
            pendientes_cerrar_stock_lines = pendientes_liquidar_line_ids.filtered(
                lambda pendientes_liquidar_line: pendientes_liquidar_line.product_id
                == invoice_line.product_id
            )
            if (
                not pendientes_cerrar_stock_lines
                or len(pendientes_cerrar_stock_lines) <= 0
            ):
                raise exceptions.ValidationError(
                    "No hay stock suficiente disponible en depósito con estos valores a liquidar. Intenta volver a comprobar el depósito"
                )
            for pendiente_stock_line in pendientes_cerrar_stock_lines:
                if invoice_line_qty > 0:
                    stock_line_reserved_qty = pendiente_stock_line.product_uom_qty
                    stock_line_done_qty = pendiente_stock_line.qty_done
                    qty_difference = invoice_line_qty - (
                        stock_line_reserved_qty - stock_line_done_qty
                    )
                    if (
                        qty_difference >= 0
                    ):  # if the invoice_qty is greater (or equal) than the available stock_qty, we close the stock_line and continue
                        pendiente_stock_line.write(
                            {'qty_done': stock_line_reserved_qty}
                        )
                    else:
                        pendiente_stock_line.write(
                            {'qty_done': stock_line_done_qty + invoice_line_qty}
                        )
                    picking = pendiente_stock_line.picking_id
                    pickings_to_validate.add(picking)
                    invoice_line_qty = qty_difference
                else:
                    break
        # Here we validate all the pickings at once:
        for picking in pickings_to_validate:
            picking.button_validate()
            # Create backorder if necessary, because the button_validate()
            # method doesn't do it for us automaticly
            if picking._check_backorder():
                moves_to_log = {}
                for move in picking.move_lines:
                    if (
                        float_compare(
                            move.product_uom_qty,
                            move.quantity_done,
                            precision_rounding=move.product_uom.rounding,
                        )
                        > 0
                    ):
                        moves_to_log[move] = (move.quantity_done, move.product_uom_qty)
                picking._log_less_quantities_than_expected(moves_to_log)
                picking.with_context(cancel_backorder=False).action_done()
        self.action_post()

    def post_y_devolver(self):
        if not self.is_liquidacion:
            raise exceptions.ValidationError(
                "Sólo se puede devolver depósito desde una factura tipo devolución depósito en venta"
            )
        products_to_check = self.checkLiquidacionIsValid(self)
        if len(products_to_check) > 0:
            msg = "No hay stock suficiente disponible en depósito con estos valores. Estos son valores disponibles en depósito:"
            for product in products_to_check:
                msg += "\n* " + str(product[0]) + ": " + str(product[1])
            raise exceptions.UserError(msg)
        domain = [
            ('owner_id', '=', self.partner_id.id),
            (
                'location_id',
                '=',
                17,
            ),  # This is the id of the Location DS/Depósitos (the source of the move)
            (
                'location_dest_id',
                '=',
                5,
            ),  # This is the id of the Location Partner Locations/Customers (the destination of the move)
            ('state', 'in', ('assigned', 'partially_available')),
        ]
        pendientes_liquidar_line_ids = self.env['stock.move.line'].search(
            domain, order='date asc'
        )  # deposito de este contacto
        pickings_to_assign = set()
        pickings_return = (
            {}
        )  # relation between done_picking (key) and the created_return (value)
        for invoice_line in self.invoice_line_ids:
            liquidacion_line_qty = invoice_line.quantity
            if liquidacion_line_qty > 0.0:
                pendientes_cerrar_stock_lines = pendientes_liquidar_line_ids.filtered(
                    lambda pendientes_liquidar_line: pendientes_liquidar_line.product_id
                    == invoice_line.product_id
                )
                if (
                    not pendientes_cerrar_stock_lines
                    or len(pendientes_cerrar_stock_lines) <= 0
                ):
                    raise exceptions.ValidationError(
                        "No hay stock suficiente disponible en depósito para devolver. Intenta volver a comprobar el depósito"
                    )
                for pendiente_stock_line in pendientes_cerrar_stock_lines:
                    if liquidacion_line_qty <= 0:
                        break
                    stock_line_reserved_qty = pendiente_stock_line.product_uom_qty
                    stock_line_done_qty = pendiente_stock_line.qty_done
                    qty_deposito = stock_line_reserved_qty - stock_line_done_qty
                    qty_difference = liquidacion_line_qty - qty_deposito
                    # if the liquidacion_qty is greater (or equal) than the available qty_deposito,
                    # we look for the associated stock.picking that enabled the current move.line de depósito,
                    # and then we return an amount of qty_deposito of the product_id on the associated stock.picking

                    pickings_to_assign.add(
                        pendiente_stock_line.picking_id
                    )  # associated deposito picking

                    associated_done_picking = (
                        pendiente_stock_line.picking_id.sale_id.picking_ids.filtered(
                            lambda picking: picking.location_id.id == 8
                            and picking.location_dest_id.id == 17
                            and picking.state == 'done'
                            and invoice_line.product_id.id
                            in [
                                li.product_id.id
                                for li in picking.move_line_ids_without_package
                            ]
                        )
                    )
                    if len(associated_done_picking) > 1:
                        associated_done_picking = associated_done_picking[0]
                    # Check if we have already created a return for this done_picking
                    if associated_done_picking not in pickings_return:
                        # New Wizard to make the return of one line
                        return_picking = self.env['stock.return.picking'].create(
                            {'picking_id': associated_done_picking.id}
                        )
                        pickings_return[associated_done_picking] = return_picking
                        return_picking._onchange_picking_id()  # what does this do?
                    return_picking = pickings_return.get(associated_done_picking)
                    # Correct the lines with negative prohibited values
                    for line in return_picking.product_return_moves:
                        if line.quantity < 0:
                            line.write({'quantity': 0})

                    return_picking_line = return_picking.product_return_moves.filtered(
                        lambda line: line.product_id == invoice_line.product_id
                    )
                    return_qty = (
                        qty_deposito if qty_difference >= 0 else liquidacion_line_qty
                    )
                    get_qty = return_picking_line.quantity
                    return_picking_line.write(
                        {'quantity': get_qty + return_qty}
                    )  # we add to the existing value
                    liquidacion_line_qty = qty_difference
        for return_picking in pickings_return.values():
            new_stock_picking_data = return_picking.create_returns()
            new_stock_picking = self.env['stock.picking'].browse(
                new_stock_picking_data['res_id']
            )
            for line in new_stock_picking.move_ids_without_package:
                line.write({'quantity_done': line.product_uom_qty})
            new_stock_picking.button_validate()
        for picking in pickings_to_assign:
            # Check availavility to load again the stock.move.lines after the return
            picking.action_assign()
        _logger.debug(
            "***************************************************** post_y_devolver "
        )
        self.action_post()


class EditorialAccountMoveLine(models.Model):
    """ Extend account.move.line template for editorial management """

    _description = "Editorial Account Move Line"
    _inherit = 'account.move.line'  # odoo/addons/account/models/account_move.py

    product_barcode = fields.Char(
        string="Código de barras / ISBN", related='product_id.barcode', readonly=True
    )
