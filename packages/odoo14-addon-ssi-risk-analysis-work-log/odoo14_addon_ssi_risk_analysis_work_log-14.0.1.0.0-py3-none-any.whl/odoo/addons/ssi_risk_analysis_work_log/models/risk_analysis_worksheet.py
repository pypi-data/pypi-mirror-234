# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class RiskAnalysisWorksheet(models.Model):
    _name = "risk_analysis_worksheet"
    _inherit = [
        "risk_analysis_worksheet",
        "mixin.work_object",
    ]

    _work_log_create_page = True
