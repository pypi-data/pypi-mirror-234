# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class QCWorksheet(models.Model):
    _name = "qc_worksheet"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_ready",
        "mixin.transaction_open",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.transaction_terminate",
    ]
    _description = "QC Worksheet"

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

    @api.model
    def _default_model_id(self):
        model = False
        obj_ir_model = self.env["ir.model"]
        model_name = self.env.context.get("quality_control_model", False)
        if model_name:
            criteria = [("model", "=", model_name)]
            model = obj_ir_model.search(criteria)
        return model

    model_id = fields.Many2one(
        string="Document Type",
        comodel_name="ir.model",
        index=True,
        required=True,
        ondelete="cascade",
        default=lambda self: self._default_model_id(),
        readonly=True,
    )
    model_name = fields.Char(
        related="model_id.model",
        index=True,
        store=True,
    )
    object_id = fields.Many2oneReference(
        string="Document ID",
        index=True,
        required=True,
        readonly=False,
        model_field="model_name",
    )

    @api.model
    def _selection_target_model(self):
        return [(model.model, model.name) for model in self.env["ir.model"].search([])]

    @api.depends(
        "model_id",
        "object_id",
    )
    def _compute_object_reference(self):
        for document in self:
            result = False
            if document.model_id and document.object_id:
                result = "%s,%s" % (document.model_name, document.object_id)
            document.object_reference = result

    object_reference = fields.Reference(
        string="Document Reference",
        compute="_compute_object_reference",
        store=True,
        selection="_selection_target_model",
    )

    date = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="qc_worksheet_type",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    question_ids = fields.One2many(
        string="Questions",
        comodel_name="qc_worksheet.question",
        inverse_name="worksheet_id",
    )
    result = fields.Boolean(
        string="Result",
        compute="_compute_result",
        store=True,
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
        res = super(QCWorksheet, self)._get_policy_field()
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
        "question_ids",
        "question_ids.success",
    )
    def _compute_result(self):
        for record in self:
            result = True
            for question in record.question_ids:
                if not question.success:
                    result = False
                    continue
            record.result = result

    def action_reload_question(self):
        for record in self.sudo():
            record._reload_question()

    def _reload_question(self):
        self.ensure_one()
        self.question_ids.unlink()
        for question in self.type_id.question_ids:
            question._create_worksheet_question(self)
