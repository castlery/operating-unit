# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import _, api, fields, models
from openerp.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def _default_section_id(self):
        """ Gives default section by checking if present in the context """
        section_id = self._resolve_section_id_from_context() or False
        if not section_id:
            section_id = self.env.user.default_section_id or False
        return section_id

    @api.model
    def _default_operating_unit(self):
        if self._default_section_id():
            return self.env['crm.case.section'].browse(self._defaults['section_id']()).operating_unit_id
        else:
            return self.env.user.default_operating_unit_id

    operating_unit_id = fields.Many2one(
        comodel_name='operating.unit',
        string='Operating Unit',
        default=_default_operating_unit
    )

    @api.multi
    @api.constrains('operating_unit_id', 'company_id')
    def _check_company_operating_unit(self):
        for rec in self:
            if (rec.company_id and rec.operating_unit_id and
                    rec.company_id != rec.operating_unit_id.company_id):
                raise ValidationError(_('Configuration error\nThe Company in'
                                        ' the Sales Order and in the Operating'
                                        ' Unit must be the same.'))

    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        invoice_vals = super(SaleOrder, self)._prepare_invoice(cr, uid, order, lines, context=context)
        invoice_vals['operating_unit_id'] = order.operating_unit_id.id
        return invoice_vals


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    operating_unit_id = fields.Many2one(related='order_id.operating_unit_id',
                                        string='Operating Unit',
                                        readonly=True, store=True)
