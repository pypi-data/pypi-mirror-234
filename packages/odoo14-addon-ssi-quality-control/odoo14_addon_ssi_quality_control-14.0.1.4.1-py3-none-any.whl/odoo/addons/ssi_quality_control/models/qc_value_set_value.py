# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class QCValueSetValue(models.Model):
    _name = "qc_value_set.value"
    _description = "QC Value Set - Value"

    set_id = fields.Many2one(
        string="Value Set",
        comodel_name="qc_value_set",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    item_id = fields.Many2one(
        string="Item",
        comodel_name="qc_value_item",
        required=True,
        ondelete="restrict",
    )
    ok = fields.Boolean(
        string="Correct Answer",
    )
