# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class RiskAnalysis(models.Model):
    _name = "risk_analysis"
    _inherit = [
        "risk_analysis",
        "mixin.responsible_task",
    ]

    _responsible_task_create_page = True
