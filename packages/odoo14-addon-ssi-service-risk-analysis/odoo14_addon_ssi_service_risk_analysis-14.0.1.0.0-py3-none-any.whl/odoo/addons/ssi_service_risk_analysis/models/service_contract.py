# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class ServiceContract(models.Model):
    _name = "service.contract"
    _inherit = [
        "service.contract",
        "mixin.risk_analysis",
    ]
    _risk_analysis_create_page = True
    _risk_analysis_partner_field_name = "partner_id"
