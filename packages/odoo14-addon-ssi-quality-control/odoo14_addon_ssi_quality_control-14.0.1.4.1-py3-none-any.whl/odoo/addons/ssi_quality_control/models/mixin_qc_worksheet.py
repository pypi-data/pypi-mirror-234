# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class MixinQCWorksheet(models.AbstractModel):
    _name = "mixin.qc_worksheet"
    _description = "QC Worksheet Mixin"

    _qc_worksheet_create_page = False
    _qc_worksheet_page_xpath = "//page[last()]"

    qc_result_computation_method = fields.Selection(
        string="QC Result Computation Method",
        selection=[
            ("auto", "Automatic"),
            ("manual", "Manual"),
        ],
        default="auto",
        required=True,
    )
    qc_auto_result = fields.Boolean(
        string="QC Automatic Result",
        compute="_compute_qc_result",
        store=True,
    )
    qc_manual_result = fields.Boolean(
        string="QC Manual Result",
    )
    qc_final_result = fields.Boolean(
        string="QC Final Result",
        compute="_compute_qc_result",
        store=True,
    )
    qc_worksheet_set_id = fields.Many2one(
        string="Worksheet Set",
        comodel_name="qc_worksheet_set",
    )
    qc_worksheet_ids = fields.One2many(
        string="QC Worksheets",
        comodel_name="qc_worksheet",
        inverse_name="object_id",
        domain=lambda self: [("model_name", "=", self._name)],
        auto_join=True,
        readonly=False,
    )

    @api.depends(
        "qc_result_computation_method",
        "qc_manual_result",
        "qc_worksheet_ids",
        "qc_worksheet_ids.state",
        "qc_worksheet_ids.result",
    )
    def _compute_qc_result(self):
        for record in self:
            automatic_result = final_result = True

            for worksheet in record.qc_worksheet_ids:
                if worksheet.state != "done":
                    automatic_result = False
                    continue

                if not worksheet.result:
                    automatic_result = False
                    continue

            if record.qc_result_computation_method == "auto":
                final_result = automatic_result
            else:
                final_result = record.qc_manual_result

            record.qc_auto_result = automatic_result
            record.qc_final_result = final_result

    @ssi_decorator.insert_on_form_view()
    def _qc_worksheet_insert_form_element(self, view_arch):
        if self._qc_worksheet_create_page:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id="ssi_quality_control.qc_worksheet_page",
                xpath=self._qc_worksheet_page_xpath,
                position="after",
            )
        return view_arch

    def unlink(self):
        qc_worksheet_ids = self.mapped("qc_worksheet_ids")
        qc_worksheet_ids.unlink()
        return super(MixinQCWorksheet, self).unlink()

    def action_open_qc_worksheet(self):
        for record in self.sudo():
            result = record._open_qc_worksheet()
        return result

    def action_create_qc_worksheet(self):
        for record in self.sudo():
            record._create_qc_worksheet()

    def _open_qc_worksheet(self):
        self.ensure_one()

        waction = self.env.ref("ssi_quality_control.qc_worksheet_action").read()[0]
        waction.update({"domain": [("id", "in", self.qc_worksheet_ids.ids)]})
        return waction

    def _create_qc_worksheet(self):
        self.ensure_one()

        if not self.qc_worksheet_set_id:
            return True

        if self.qc_worksheet_ids:
            return True

        for worksheet_type in self.qc_worksheet_set_id.type_ids:
            worksheet_type._create_worksheet(self)

        if self.qc_worksheet_ids:
            self.qc_worksheet_ids.action_reload_question()
