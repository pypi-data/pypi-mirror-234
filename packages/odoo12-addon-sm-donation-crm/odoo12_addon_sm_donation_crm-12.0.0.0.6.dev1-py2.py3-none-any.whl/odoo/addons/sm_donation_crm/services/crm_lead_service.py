import json

from odoo.exceptions import ValidationError
from odoo.tools.translate import _

from odoo.addons.component.core import Component
from odoo.addons.sm_maintenance.models.models_sm_utils import sm_utils

from . import schemas

DONATION_SALES_TEAM_XML_ID = "crm_team_sales_donation"
UTM_SOURCE_DONATION_XML_ID = "utm_source_donation_main_web_page"
CRM_TYPE_OPPORTUNITY = "opportunity"
ADDON_NAME = 'sm_donation_crm'


class CrmLeadDonationService(Component):
    _inherit = "crm.lead.service"
    _name = "crm.lead.service"
    _description = "Crm lead requests"

    def _validator_create(self):
        validator_schema = super()._validator_create().copy()
        validator_schema.update(schemas.S_CRM_LEAD_CREATE)
        return validator_schema

    def _prepare_create(self, params):
        """
        Prepare data for crm lead creation
        :param dic params:
        :return:
        """
        target_source_xml_id = params.get("source_xml_id", None)

        if target_source_xml_id is None:
            return super(CrmLeadDonationService, self)._prepare_create(params)

        if target_source_xml_id == UTM_SOURCE_DONATION_XML_ID:
            create_dict = super(CrmLeadDonationService, self)._prepare_create(params)
            utm_source_record = sm_utils.get_record_by_xml_id(
                self, ADDON_NAME, UTM_SOURCE_DONATION_XML_ID)
            sales_team_record = sm_utils.get_record_by_xml_id(
                self, ADDON_NAME, DONATION_SALES_TEAM_XML_ID)
            create_dict.update({
                "source_id": utm_source_record.id,
                "type": CRM_TYPE_OPPORTUNITY,
                "team_id": sales_team_record.id
            })
            return create_dict

        return super(CrmLeadDonationService, self)._prepare_create(params)

    def create(self, **params):
        source_xml_id = params.get("source_xml_id", None)

        if source_xml_id is None:
            return super(CrmLeadDonationService, self).create(**params)

        if source_xml_id == UTM_SOURCE_DONATION_XML_ID:
            crm_lead_response = super(CrmLeadDonationService, self).create(**params)
            sales_team_record = sm_utils.get_record_by_xml_id(
                self, ADDON_NAME, DONATION_SALES_TEAM_XML_ID)
            crm_lead_data = json.loads(crm_lead_response.response[0].decode("utf-8"))
            crm_lead_id = crm_lead_data.get("id", False)

            if not crm_lead_id:
                raise ValidationError(_("Crm lead id not found in response"))

            crm_lead_record = self.env["crm.lead"].search([('id', '=', crm_lead_id)])
            crm_lead_record.write({"team_id": sales_team_record.id})
            return crm_lead_response
        return super(CrmLeadDonationService, self).create(**params)
