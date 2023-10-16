# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, models


class ServiceQuotation(models.Model):
    _name = "service.quotation"
    _inherit = [
        "service.quotation",
    ]

    @api.onchange(
        "lead_id",
        "partner_id",
    )
    def onchange_risk_analysis_id(self):
        self.risk_analysis_id = False
        if self.lead_id:
            self.risk_analysis_id = self.lead_id.risk_analysis_id
