from odoo import fields, models


class UtmSource(models.Model):
    """
    Add the field if a UTM Source is of type onboarding
    """
    _inherit = 'utm.source'
    is_onboarding = fields.Boolean('is onboarding?', default=False)

