# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import _, api, fields, models
from openerp.exceptions import ValidationError, Warning


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    operating_unit_id = fields.Many2one(
        comodel_name='operating.unit',
        string='Operating Unit',
        required=True, select=1, states={'confirmed': [('readonly', True)], 'approved': [('readonly', True)]},
        default=lambda self: (self.env['res.users'].
                              operating_unit_default_get(self.env.uid))
    )

    @api.constrains('operating_unit_id', 'company_id')
    def _check_company_operating_unit(self):
        for record in self:
            if (record.company_id and record.operating_unit_id and
                    record.company_id != record.operating_unit_id.company_id):
                raise ValidationError(
                    _('Configuration error\nThe Company in the Purchase Order '
                      'and in the Operating Unit must be the same.')
                )

    def _prepare_inv_line(self, cr, uid, account_id, order_line, context=None):
        inv_line_vals = super(PurchaseOrder, self)._prepare_inv_line(cr, uid, account_id, order_line, context=context)
        inv_line_vals['operating_unit_id'] = order_line.operating_unit_id.id
        return inv_line_vals

    def _prepare_invoice(self, cr, uid, order, line_ids, context=None):
        invoice_vals = super(PurchaseOrder, self)._prepare_invoice(cr, uid, order, line_ids, context=context)
        invoice_vals['operating_unit_id'] = order.operating_unit_id.id
        return invoice_vals

    @api.model
    def _prepare_picking(self):
        picking_vals = super(PurchaseOrder, self)._prepare_picking()
        picking_vals['operating_unit_id'] = self.operating_unit_id.id
        return picking_vals


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    operating_unit_id = fields.Many2one(related='order_id.operating_unit_id',
                                        string='Operating Unit', readonly=True, store=True)

    @api.constrains('operating_unit_id', 'invoice_lines')
    def _check_invoice_ou(self):
        for line in self:
            for inv_line in line.invoice_lines:
                invoice_operating_unit = inv_line.invoice_id.operating_unit_id
                if (inv_line.invoice_id and
                        invoice_operating_unit != line.operating_unit_id):
                    raise ValidationError(
                        _('The operating unit of the purchase order must '
                          'be the same as in the associated invoices.')
                    )
