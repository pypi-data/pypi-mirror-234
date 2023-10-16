# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class MixinRiskAnalysis(models.AbstractModel):
    _name = "mixin.risk_analysis"
    _inherit = [
        "mixin.decorator",
    ]
    _description = "Mixin for Object With Risk Analysis"
    _risk_analysis_create_page = False
    _risk_analysis_page_xpath = "//page[last()]"
    _risk_analysis_partner_field_name = False

    allowed_risk_analysis_ids = fields.Many2many(
        string="Allowed Risk Analysis",
        comodel_name="risk_analysis",
        compute="_compute_allowed_risk_analysis_ids",
        store=False,
    )
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
        compute_sudo=True,
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

    def onchange_risk_analysis_id(self):
        self.risk_analysis_id = False

    def _get_allowed_risk_analysis_ids_trigger(self):
        result = []
        if self._risk_analysis_partner_field_name:
            result += [self._risk_analysis_partner_field_name]
        return result

    @api.depends(lambda self: self._get_allowed_risk_analysis_ids_trigger())
    def _compute_allowed_risk_analysis_ids(self):
        for record in self:
            result = []
            if self._risk_analysis_partner_field_name and hasattr(
                record, self._risk_analysis_partner_field_name
            ):
                partner = getattr(record, self._risk_analysis_partner_field_name)
                if partner:
                    criteria = [
                        ("partner_id", "=", partner.commercial_partner_id.id),
                        ("state", "!=", "cancel"),
                    ]
                    result = self.env["risk_analysis"].search(criteria).ids
            record.allowed_risk_analysis_ids = result

    @ssi_decorator.insert_on_form_view()
    def _risk_analysis_insert_form_element(self, view_arch):
        if self._risk_analysis_create_page:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id="ssi_risk_analysis.risk_analysis",
                xpath=self._risk_analysis_page_xpath,
                position="after",
            )
        return view_arch
