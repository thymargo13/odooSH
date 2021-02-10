# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_round
from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.tools.float_utils import float_compare
from werkzeug import urls
import json
import requests
from requests.exceptions import HTTPError
import logging
import pprint

_logger = logging.getLogger(__name__)

# The following currencies are integer only, see https://opp.com/docs/currencies#zero-decimal
INT_CURRENCIES = [
    u'BIF', u'XAF', u'XPF', u'CLP', u'KMF', u'DJF', u'GNF', u'JPY', u'MGA', u'PYG', u'RWF', u'KRW',
    u'VUV', u'VND', u'XOF'
]


class FpsPaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[
        ('fps', 'FPS')
    ], default='fps', ondelete={'fps': 'set default'})
    fps_secret_key = fields.Char(
        required_if_provider='fps', groups='base.group_user')
    fps_source_sys_code = fields.Char(required_if_provider='fps')
    fps_group_code = fields.Char(required_if_provider='fps')
    fps_pay_method = fields.Char(required_if_provider='fps', default="FPS")

    @api.model
    def _create_missing_journal_for_acquirers(self, company=None):
        # By default, the wire transfer method uses the default Bank journal.
        company = company or self.env.company
        acquirers = self.env['payment.acquirer'].search(
            [('provider', '=', 'fps'), ('journal_id', '=', False), ('company_id', '=', company.id)])

        bank_journal = self.env['account.journal'].search(
            [('type', '=', 'bank'), ('company_id', '=', company.id)], limit=1)
        if bank_journal:
            acquirers.write({'journal_id': bank_journal.id})
        return super(FpsPaymentAcquirer, self)._create_missing_journal_for_acquirers(company=company)

    def fps_get_form_action_url(self):
        self.ensure_one()
        _logger.info("txn get form action_url")
        return urls.url_join(self._get_opp_api_url(), 'api/oppQRCode')

    # TODO generates the values used to render the form button template.
    def fps_form_generate_values(self, values):
        _logger.info("--------------fps_form_generate_values---------------")
        _logger.info(values)
        self.ensure_one()
        base_url = self.get_base_url()

        fps_session_data = {
            'authKey': self.sudo().fps_secret_key,
            'sourceSysCode': self.sudo().fps_source_sys_code,
            'merchantRef': values['reference'],
        }

        values['session_id'] = self._create_opp_session(fps_session_data)

        #! Data Post to OPP
        params = {
            'sourceSysCode': self.sudo().fps_source_sys_code,
            'groupCode': self.sudo().fps_group_code,
            'session': values['session_id'],
            'keyNo': self.sudo().fps_secret_key,
            'order': {
                'merchantRef': values['reference'],
                'amount': int(values['amount'] if values['currency'].name in INT_CURRENCIES else float_round(values['amount'] * 100, 2)),
                'currency': values['currency'].name,
            },
        }
        fps_tx_values = {
            'jsonStr': json.dumps(params, separators=(',', ':')),
        }

        return fps_tx_values

    # * create session
    def _create_opp_session(self, kwargs):
        _logger.info("--------------FPS Create Session---------------")
        self.ensure_one()
        response = self._opp_request('api/oppCreateSessionID', kwargs)
        if response.get('result').get('result') == 'SUCCESS':
            return response.get('result').get('session').get('id')
        else:
            return response.get('data')

    def _opp_request(self, url, data=False, method='POST'):
        _logger.info("--------------FPS Call OPP ---------------")
        self.ensure_one()
        url = urls.url_join(self._get_opp_api_url(), url)
        headers = {
            'authorization': '',
            'Content-Type': 'application/json;charset=UTF-8',
        }
        resp = requests.post(url, data=json.dumps(data), headers=headers)
        if not resp.ok and (400 <= resp.status_code < 500 and resp.json().get('message', '')):
            try:
                resp.raise_for_status()
            except HTTPError:
                _logger.error(resp.text)
                opp_error = resp.json().get('error', {}).get('message', '')
                error_msg = " " + \
                    (_("Opp gave us the following info about the problem: '%s'") % opp_error)
                raise ValidationError(error_msg)
        return resp.json()

    @api.model
    def _get_opp_api_url(self):
        _logger.info("------------------Get OPP URL------------------")
        return 'http://193.112.38.50:8080/opp/'


class FpsPaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    @api.model
    # def fps_create():
    #     pass
    def fps_form_feedback(self, data):
        pass
