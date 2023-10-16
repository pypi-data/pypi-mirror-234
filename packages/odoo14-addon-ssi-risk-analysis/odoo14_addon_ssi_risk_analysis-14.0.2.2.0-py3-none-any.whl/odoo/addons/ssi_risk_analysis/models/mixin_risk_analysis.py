# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import api, fields, models


class MixinRiskAnalysis(models.AbstractModel):
    _name = "mixin.risk_analysis"
    _description = "Mixin for Object With Risk Analysis"

    risk_analysis_id = fields.Many2one(
        string="# Risk Analysis",
        comodel_name="risk_analysis",
    )
    risk_analysis_state = fields.Selection(
        related="risk_analysis_id.state",
        store=True,
    )
    risk_analysis_result_id = fields.Many2one(
        string="Risk Analysis Result",
        comodel_name="risk_analysis_result",
        compute="_compute_risk_analysis_result_id",
        store=True,
    )

    @api.depends(
        "risk_analysis_id",
        "risk_analysis_id.state",
        "risk_analysis_id.result_id",
    )
    def _compute_risk_analysis_result_id(self):
        for record in self:
            result = False
            if record.risk_analysis_id and record.risk_analysis_id.state == "done":
                result = record.risk_analysis_id.result_id
            record.risk_analysis_result_id = result
