from openerp import api, fields, models, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def invoice_pay_customer(self, cr, uid, ids, context=None):
        res = super(AccountInvoice, self).invoice_pay_customer(cr, uid, ids, context=context)
        inv = self.browse(cr, uid, ids[0], context=context)
        if 'context' in res:
            ctx = res['context']
            if inv.operating_unit_id:
                ctx['default_operating_unit_id'] = inv.operating_unit_id.id
        return res
