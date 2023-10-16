# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class RiskAnalysisWorksheet(models.Model):
    _name = "risk_analysis_worksheet"
    _description = "Risk Analysis Worksheet"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_ready",
        "mixin.transaction_open",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.transaction_terminate",
        "mixin.custom_info",
        "mixin.localdict",
    ]

    _approval_from_state = "open"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    _custom_info_create_page = False

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

    risk_analysis_id = fields.Many2one(
        string="# Risk Analysis",
        comodel_name="risk_analysis",
        readonly=True,
        required=True,
        ondelete="cascade",
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
    date = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    partner_id = fields.Many2one(
        string="Partner",
        related="risk_analysis_id.partner_id",
        store=True,
    )
    allowed_item_ids = fields.Many2many(
        string="Allowed Risk Items",
        comodel_name="risk_item",
        compute="_compute_allowed_item_ids",
        store=False,
    )
    item_id = fields.Many2one(
        string="Risk Item",
        comodel_name="risk_item",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    allowed_type_ids = fields.Many2many(
        string="Allowed Worksheet Types",
        comodel_name="risk_analysis_worksheet_type",
        compute="_compute_allowed_type_ids",
        store=False,
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="risk_analysis_worksheet_type",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    custom_info_ids = fields.One2many(
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
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
        related="item_id.allowed_result_ids",
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
        related="item_id.allowed_conclusion_ids",
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
            ("ready", "Ready To Start"),
            ("open", "In Progress"),
            ("confirm", "Waiting for Approval"),
            ("done", "Done"),
            ("reject", "Rejected"),
            ("cancel", "Cancelled"),
        ],
        copy=False,
        default="draft",
        required=True,
        readonly=True,
    )

    @api.depends(
        "risk_analysis_id",
    )
    def _compute_allowed_item_ids(self):
        for record in self:
            result = False
            if record.risk_analysis_id:
                result = self.env["risk_item"]
                for item in record.risk_analysis_id.item_ids:
                    result += item.item_id
            record.allowed_item_ids = result

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

    @api.depends(
        "item_id",
    )
    def _compute_allowed_type_ids(self):
        for record in self:
            result = False
            if record.item_id:
                criteria = [("item_id", "=", record.item_id.id)]
                result = self.env["risk_analysis_worksheet_type"].search(criteria)
            record.allowed_type_ids = result

    @api.depends(
        "manual_result_id",
        "result_computation_method",
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

    @api.onchange("risk_analysis_id")
    def onchange_item_id(self):
        self.item_id = False

    @api.onchange("item_id")
    def onchange_type_id(self):
        self.type_id = False

    @api.onchange(
        "type_id",
    )
    def onchange_custom_info_template_id(self):
        self.custom_info_template_id = False
        if self.type_id:
            self.custom_info_template_id = self.type_id.template_id

    @api.model
    def _get_policy_field(self):
        res = super(RiskAnalysisWorksheet, self)._get_policy_field()
        policy_field = [
            "ready_ok",
            "confirm_ok",
            "approve_ok",
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
