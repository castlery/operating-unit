# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# © 2015 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import api, fields, models


class CRMTeam(models.Model):
    _inherit = 'crm.case.section'

    operating_unit_id = fields.Many2one('operating.unit', 'Operating Unit',
                                        default="_default_operating_unit")

    @api.model
    def _default_operating_unit(self):
        return self.env.user.default_operating_unit_id
