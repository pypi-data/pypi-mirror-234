from odoo import api, models
from odoo.tools.translate import _

ONBOARDING_SALES_TEAM_XML_ID = "crm_team_sales_onboarding"
UTM_SOURCE_BALENYA_XML_ID = "utm_source_onboarding_company_balenya_main_web_page"
ADDON_NAME = 'sm_onboarding_crm'


class Team(models.Model):
    _name = 'crm.team'
    _inherit = 'crm.team'

    @api.model
    def action_pipeline_onboarding(self):
        return {
            "type": "ir.actions.act_window",
            "name": _("Crm: Onboarding Pipeline"),
            "view_mode": "kanban,tree,form",
            "res_model": "crm.lead",
            "target": "current",
            "context": {'default_team_id': self._get_team_sales_onboarding_id()},
            "domain": [('source_id', '=', self._get_utm_source_onboarding_id())]
        }

    def _get_team_sales_onboarding_id(self):
        return self.env.ref(f'{ADDON_NAME}.{ONBOARDING_SALES_TEAM_XML_ID}').id

    def _get_utm_source_onboarding_id(self):
        return self.env.ref(f'{ADDON_NAME}.{UTM_SOURCE_BALENYA_XML_ID}').id
