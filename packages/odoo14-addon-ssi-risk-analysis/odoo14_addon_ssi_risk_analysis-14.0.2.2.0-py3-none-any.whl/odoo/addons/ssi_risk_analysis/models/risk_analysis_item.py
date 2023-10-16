# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class RiskAnalysisItem(models.Model):
    _name = "risk_analysis.item"
    _description = "Risk Analysis Item"
    _order = "risk_analysis_id, sequence, id"

    risk_analysis_id = fields.Many2one(
        string="# Risk Analysis",
        comodel_name="risk_analysis",
        required=True,
        onldete="cascade",
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
    worksheet_id = fields.Many2one(
        string="# Worksheet",
        comodel_name="risk_analysis_worksheet",
        readonly=True,
    )
    result_id = fields.Many2one(
        related="worksheet_id.result_id",
        store=True,
    )
    allowed_result_ids = fields.Many2many(
        related="item_id.allowed_result_ids",
        store=False,
    )
    quantitative_value = fields.Float(
        string="Quantitative Value",
        required=True,
        default=0.0,
    )

    @api.onchange("item_id")
    def onchange_result_id(self):
        self.result_id = False

    @api.onchange(
        "result_id",
    )
    def onchange_quantitative_value(self):
        self.quantitative_value = 0.0
        if self.result_id and self.item_id:
            criteria = [
                ("item_id", "=", self.item_id.id),
                ("result_id", "=", self.result_id.id),
            ]
            results = self.env["risk_item.result"].search(criteria)
            if len(results) > 0:
                self.quantitative_value = results[0].quantitative_value

    def action_get_worksheet(self):
        for record in self:
            record._get_worksheet()

    def _get_worksheet(self):
        self.ensure_one()
        criteria = [
            ("risk_analysis_id", "=", self.risk_analysis_id.id),
            ("item_id", "=", self.item_id.id),
        ]
        results = self.env["risk_analysis_worksheet"].search(criteria)

        if len(results) > 0:
            self.write({"worksheet_id": results[0].id})
