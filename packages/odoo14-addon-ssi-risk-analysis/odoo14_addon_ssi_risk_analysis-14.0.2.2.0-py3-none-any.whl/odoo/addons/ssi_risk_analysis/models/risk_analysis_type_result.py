# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class RiskAnalysisTypeResult(models.Model):
    _name = "risk_analysis_type.result"
    _description = "Risk Analysis Type -  Result"
    _order = "type_id, sequence, id"

    type_id = fields.Many2one(
        string="Type",
        comodel_name="risk_analysis_type",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
    )
    result_id = fields.Many2one(
        string="Result",
        comodel_name="risk_analysis_result",
        required=True,
        onldete="restrict",
    )
    quantitative_value = fields.Float(
        string="Quantitative Value",
        required=True,
        default=0.0,
    )
