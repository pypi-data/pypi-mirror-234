# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class RiskAnalysisWorkSheetType(models.Model):
    _name = "risk_analysis_worksheet_type"
    _inherit = ["mixin.master_data"]
    _description = "Risk Analysis Worksheet Type"

    item_id = fields.Many2one(
        string="Risk Item",
        comodel_name="risk_item",
        required=True,
    )
    ttype = fields.Selection(
        string="Type",
        selection=[
            ("standard", "Standard"),
            ("custom", "Custom"),
        ],
        default="standard",
        required=True,
    )
    template_id = fields.Many2one(
        string="Template",
        comodel_name="custom_info.template",
    )
    model_id = fields.Many2one(
        string="Model",
        comodel_name="ir.model",
    )
    model = fields.Char(
        string="Model Technical Name",
        related="model_id.model",
    )
    result_python_code = fields.Text(
        string="Python Code for Result Computation",
        default="result = False",
        required=True,
    )

    @api.onchange(
        "ttype",
    )
    def onchange_model_id(self):
        self.model_id = False

    @api.onchange(
        "ttype",
    )
    def onchange_template_id(self):
        self.template_id = False
