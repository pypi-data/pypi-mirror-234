from odoo import fields, models


class Directory(models.Model):
    _inherit = "dms.directory"

    expiry_date = fields.Date(string="Expiry Date")
    code = fields.Char("code")
