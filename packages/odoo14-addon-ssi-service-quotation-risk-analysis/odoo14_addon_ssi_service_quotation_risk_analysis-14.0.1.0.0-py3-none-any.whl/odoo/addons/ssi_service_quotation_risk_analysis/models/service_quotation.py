# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class ServiceQuotation(models.Model):
    _name = "service.quotation"
    _inherit = [
        "service.quotation",
        "mixin.risk_analysis",
    ]
    _risk_analysis_create_page = True
    _risk_analysis_partner_field_name = "partner_id"

    def _prepare_contract_data(self):
        self.ensure_one()
        _super = super(ServiceQuotation, self)
        result = _super._prepare_contract_data()
        result.update(
            {
                "risk_analysis_id": self.risk_analysis_id
                and self.risk_analysis_id.id
                or False,
            }
        )
        return result
