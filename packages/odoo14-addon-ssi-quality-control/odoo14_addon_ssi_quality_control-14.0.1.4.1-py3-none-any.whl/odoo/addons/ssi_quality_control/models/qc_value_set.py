# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class QCValueSet(models.Model):
    _name = "qc_value_set"
    _inherit = ["mixin.master_data"]
    _description = "QC Value Set"

    value_ids = fields.One2many(
        string="Values",
        comodel_name="qc_value_set.value",
        inverse_name="set_id",
    )
