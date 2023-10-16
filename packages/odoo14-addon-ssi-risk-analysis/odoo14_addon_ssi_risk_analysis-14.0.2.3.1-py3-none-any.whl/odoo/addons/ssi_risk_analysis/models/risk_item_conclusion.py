# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class RiskItemConclusion(models.Model):
    _name = "risk_item.conclusion"
    _description = "Risk Item Conclusion"
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
    conclusion_id = fields.Many2one(
        string="Conclusion",
        comodel_name="risk_analysis_conclusion",
        required=True,
        onldete="restrict",
    )
