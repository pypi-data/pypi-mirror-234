# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class RiskItemResult(models.Model):
    _name = "risk_item.result"
    _description = "Risk Item Result"
    _order = "item_id, sequence, id"

    item_id = fields.Many2one(
        string="Item",
        comodel_name="risk_item",
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
