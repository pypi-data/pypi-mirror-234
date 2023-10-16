# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ServiceQuotation(models.Model):
    _name = "service.quotation"
    _inherit = [
        "service.quotation",
    ]

    lead_id = fields.Many2one(
        string="# Lead",
        comodel_name="crm.lead",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    allowed_quotation_ids = fields.Many2many(
        string="Allowed Quotations",
        comodel_name="crm.lead",
        compute="_compute_allowed_quotation_ids",
        compute_sudo=True,
    )

    @api.depends(
        "partner_id",
    )
    def _compute_allowed_quotation_ids(self):
        for record in self:
            result = []
            if record.partner_id:
                criteria = [
                    ("partner_id.commercial_partner_id", "=", record.partner_id.id)
                ]
                result = self.env["crm.lead"].search(criteria).ids
            record.allowed_quotation_ids = result
