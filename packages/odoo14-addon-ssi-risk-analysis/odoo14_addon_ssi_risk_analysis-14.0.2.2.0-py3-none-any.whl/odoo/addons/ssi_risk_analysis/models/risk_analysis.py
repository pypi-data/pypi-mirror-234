# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class RiskAnalysis(models.Model):
    _name = "risk_analysis"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_ready",
        "mixin.transaction_open",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.transaction_terminate",
        "mixin.localdict",
    ]
    _description = "Risk Analysis"

    # Multiple Approval Attribute
    _approval_from_state = "open"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False

    _statusbar_visible_label = "draft,ready,open,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "open_ok",
        "done_ok",
        "restart_approval_ok",
        "cancel_ok",
        "terminate_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_ready",
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "action_open",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "%(ssi_transaction_terminate_mixin.base_select_terminate_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_ready",
        "dom_open",
        "dom_done",
        "dom_cancel",
        "dom_terminate",
    ]

    # Sequence attribute
    _create_sequence_state = "ready"

    date = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        required=True,
        readonly=True,
        domain=[
            "|",
            "&",
            ("parent_id", "=", False),
            ("is_company", "=", False),
            ("is_company", "=", True),
        ],
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="risk_analysis_type",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    reviewer_id = fields.Many2one(
        string="Reviewer",
        comodel_name="res.users",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    work_hour = fields.Float(
        string="Work Hours",
    )
    reviewer_work_hour = fields.Float(
        string="Reviewer Work Hours",
    )
    item_ids = fields.One2many(
        string="Risk Items",
        comodel_name="risk_analysis.item",
        inverse_name="risk_analysis_id",
        readonly=True,
    )
    result_computation_method = fields.Selection(
        string="Result Computation Method",
        selection=[
            ("manual", "Manual"),
            ("auto", "Automatic"),
        ],
        required=True,
        default="manual",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    allowed_result_ids = fields.Many2many(
        string="Allowed Risk Analysis Results",
        related="type_id.allowed_result_ids",
        store=False,
    )
    result_id = fields.Many2one(
        string="Final Result",
        comodel_name="risk_analysis_result",
        compute="_compute_result_id",
        store=True,
    )
    manual_result_id = fields.Many2one(
        string="Manual Result",
        comodel_name="risk_analysis_result",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    automatic_result_id = fields.Many2one(
        string="Automatic Result",
        comodel_name="risk_analysis_result",
        compute="_compute_result_id",
        store=True,
    )
    need_dissenting_reason = fields.Boolean(
        string="Need Dissenting Reason",
        compute="_compute_need_dissenting_reason",
        store=True,
    )
    dissenting_reason = fields.Text(
        string="Dissenting Reason",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    allowed_conclusion_ids = fields.Many2many(
        string="Allowed Risk Analysis Conclusions",
        related="type_id.allowed_conclusion_ids",
        store=False,
    )
    conclusion_id = fields.Many2one(
        string="Conclusion",
        comodel_name="risk_analysis_conclusion",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    conclusion = fields.Text(
        string="Conclusion Reasoning",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("ready", "Ready to Start"),
            ("open", "In Progress"),
            ("confirm", "Waiting for Approval"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
            ("reject", "Rejected"),
            ("terminate", "Terminated"),
        ],
        default="draft",
        copy=False,
    )

    @api.model
    def _get_policy_field(self):
        res = super(RiskAnalysis, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "ready_ok",
            "open_ok",
            "done_ok",
            "cancel_ok",
            "terminate_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @api.depends(
        "manual_result_id",
        "result_computation_method",
        "item_ids",
        "item_ids.result_id",
        "item_ids.worksheet_id.state",
        "type_id",
    )
    def _compute_result_id(self):
        for record in self:
            automatic_result = final_result = False

            automatic_result = record._get_automatic_result()

            if record.result_computation_method == "manual":
                final_result = record.manual_result_id
            elif record.result_computation_method == "auto":
                final_result = automatic_result

            record.automatic_result_id = automatic_result
            record.result_id = final_result

    @api.depends(
        "manual_result_id",
        "automatic_result_id",
    )
    def _compute_need_dissenting_reason(self):
        for record in self:
            result = False
            if record.manual_result_id != record.automatic_result_id:
                result = True
            record.need_dissenting_reason = result

    @api.onchange(
        "type_id",
    )
    def onchange_policy_template_id(self):
        self.policy_template_id = False

    def action_reload_risk_item(self):
        for record in self:
            record._reload_risk_item()

    def _reload_risk_item(self):
        self.ensure_one()
        self.item_ids.unlink()
        if self.type_id and self.type_id.item_ids:
            for item in self.type_id.item_ids:
                item._create_risk_analysis_item(self)

    def _get_automatic_result(self):
        self.ensure_one()
        localdict = self._get_default_localdict()
        try:
            safe_eval(
                self.type_id.result_python_code,
                localdict,
                mode="exec",
                nocopy=True,
            )
            result = localdict["result"]
        except Exception:
            result = False
        return result
