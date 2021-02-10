# -*- coding: utf-8 -*-
import logging
import pprint
import werkzeug

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class FPSController(http.Controller):
    _accept_url = '/payment/fps/notify'
    return_url = '/payment/fps/return'
    tx_url = '/payment/fps/qrcode'

    # TODO validate the order payment
    def _fps_validate_data(self, **post):
        pass

    # ! api for opp to call back
    @http.route('/payment/fps/return', type='http', auth="public", methods=['GET', 'POST'])
    def fps_return(self, **post):
        """ FPS return """
        _logger.info('Beginning FPS form_feedback with post data %s',
                     pprint.pformat(post))
        self._fps_validate_data(**post)
        return werkzeug.utils.redirect('/payment/process')

    @http.route('/payment/fps/qrcode', type='http', auth="public", website=True)
    def fps_qrcode(self, **post):
        """Display QR Code"""
        _logger.info('Beginning Generate QR code pages')
        return http.request.render('payment_fps.qr_code', {})
