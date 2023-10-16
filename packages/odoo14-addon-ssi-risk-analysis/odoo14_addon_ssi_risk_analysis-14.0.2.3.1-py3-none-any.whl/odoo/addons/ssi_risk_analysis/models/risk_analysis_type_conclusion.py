# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class RiskAnalysisTypeConclusion(models.Model):
    _name = "risk_analysis_type.conclusion"
    _description = "Risk Analysis Type -  Conclusion"
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
    conclusion_id = fields.Many2one(
        string="Conclusion",
        comodel_name="risk_analysis_conclusion",
        required=True,
        onldete="restrict",
    )
