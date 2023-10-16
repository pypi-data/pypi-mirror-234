from odoo import api, models
from odoo.tools.translate import _

UTM_SOURCE_DONATION_XML_ID = "utm_source_donation_main_web_page"
ADDON_NAME = 'sm_donation_crm'
CRM_TEAM_SALES_DONATION_XML_ID = "crm_team_sales_donation"


class Team(models.Model):
    _name = 'crm.team'
    _inherit = 'crm.team'

    @api.model
    def action_pipeline_donation(self):
        return {
            "type": "ir.actions.act_window",
            "name": _("Crm: Donation Pipeline"),
            "view_mode": "kanban,tree,form",
            "res_model": "crm.lead",
            "target": "current",
            "context": {'default_team_id': self._get_team_sales_donation_id()},
            "domain": [('source_id', '=', self._get_utm_source_donation_id())]
        }

    def _get_team_sales_donation_id(self):
        return self.env.ref(f'{ADDON_NAME}.{CRM_TEAM_SALES_DONATION_XML_ID}').id

    def _get_utm_source_donation_id(self):
        return self.env.ref(f'{ADDON_NAME}.{UTM_SOURCE_DONATION_XML_ID}').id
