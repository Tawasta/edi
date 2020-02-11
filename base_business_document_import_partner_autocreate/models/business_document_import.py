# -*- coding: utf-8 -*-
import logging
from openerp import models, _, api
from openerp.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class BusinessDocumentImport(models.AbstractModel):
    _inherit = 'business.document.import'

    @api.model
    def _match_partner(
            self, partner_dict, chatter_msg, partner_type='supplier'):
        """
        If partner is not found, auto-create one
        """
        try:
            # Try to match the partner
            return super(BusinessDocumentImport, self)._match_partner(
                partner_dict=partner_dict,
                chatter_msg=chatter_msg,
                partner_type=partner_type,
            )
        except ValidationError, e:
            # Partner can't be matched. Try to create a new one
            _logger.warning(e)
            res_partner = self.env['res.partner']

            partner = res_partner.create(partner_dict)

            if partner:
                return partner
            else:
                raise ValidationError(_("Could not create a partner"))
