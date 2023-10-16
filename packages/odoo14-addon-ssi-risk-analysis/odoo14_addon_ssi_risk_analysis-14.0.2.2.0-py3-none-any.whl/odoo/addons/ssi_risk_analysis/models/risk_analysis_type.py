# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class RiskAnalysisType(models.Model):
    _name = "risk_analysis_type"
    _inherit = ["mixin.master_data"]
    _description = "Risk Analysis Type"

    item_ids = fields.One2many(
        string="Risk Items",
        comodel_name="risk_analysis_type.item",
        inverse_name="type_id",
    )
    result_ids = fields.One2many(
        string="Risk Analysis Results",
        comodel_name="risk_analysis_type.result",
        inverse_name="type_id",
    )
    allowed_result_ids = fields.Many2many(
        string="Allowed Risk Analysis Results",
        comodel_name="risk_analysis_result",
        compute="_compute_allowed_result_ids",
        store=False,
    )
    result_python_code = fields.Text(
        string="Python Code for Result Computation",
        default="result = False",
        required=True,
    )
    conclusion_ids = fields.One2many(
        string="Risk Analysis Conclusions",
        comodel_name="risk_analysis_type.conclusion",
        inverse_name="type_id",
    )
    allowed_conclusion_ids = fields.Many2many(
        string="Allowed Risk Analysis Conclusions",
        comodel_name="risk_analysis_conclusion",
        compute="_compute_allowed_conclusion_ids",
        store=False,
    )

    def _compute_allowed_result_ids(self):
        for record in self:
            result = self.env["risk_analysis_result"]
            for ra_result in record.result_ids:
                result += ra_result.result_id
            record.allowed_result_ids = result

    def _compute_allowed_conclusion_ids(self):
        for record in self:
            result = self.env["risk_analysis_conclusion"]
            for ra_conclusion in record.conclusion_ids:
                result += ra_conclusion.conclusion_id
            record.allowed_conclusion_ids = result
