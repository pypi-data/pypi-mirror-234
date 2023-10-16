# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class RiskAnalysisTypeItem(models.Model):
    _name = "risk_analysis_type.item"
    _description = "Risk Analysis Type"
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
    item_id = fields.Many2one(
        string="Risk Item",
        comodel_name="risk_item",
        required=True,
        onldete="restrict",
    )

    def _create_risk_analysis_item(self, risk_analysis):
        self.ensure_one()
        self.env["risk_analysis.item"].create(
            self._prepare_risk_analysis_item(risk_analysis)
        )

    def _prepare_risk_analysis_item(self, risk_analysis):
        self.ensure_one()
        return {
            "risk_analysis_id": risk_analysis.id,
            "sequence": self.sequence,
            "item_id": self.item_id.id,
        }
