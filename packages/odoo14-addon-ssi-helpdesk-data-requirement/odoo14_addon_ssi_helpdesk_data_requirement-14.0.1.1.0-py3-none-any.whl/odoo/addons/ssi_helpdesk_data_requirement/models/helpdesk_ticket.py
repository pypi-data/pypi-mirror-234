# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class HelpdeskTicket(models.Model):
    _name = "helpdesk_ticket"
    _inherit = [
        "helpdesk_ticket",
        "mixin.data_requirement",
    ]
    _data_requirement_create_page = True
    _data_requirement_configurator_field_name = "type_id"
    _data_requirement_partner_field_name = "commercial_partner_id"
    _data_requirement_contact_field_name = "partner_id"

    data_requirement_ids = fields.Many2many(
        relation="rel_ticket_2_data_requirement",
        column1="ticket_id",
        column2="data_requirement_id",
    )
