from odoo import models, fields


class Category(models.Model):
    _inherit = "dms.category"

    expiry_date = fields.Boolean(string="Expiry date")
    expiry_self_check = fields.Boolean(string="Expiry self-check")
    auto_send_email = fields.Boolean(string="Auto send email")
    template_email_id = fields.Many2one("mail.template", string="Email template")
