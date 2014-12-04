# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from venda_app.venda_model import Venda
from routes.vendas.new import index, save
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        template_response = index()
        self.assert_can_render(template_response)


class SaveTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Venda.query().get())
        redirect_response = save(preco='1.01')
        self.assertIsInstance(redirect_response, RedirectResponse)
        saved_venda = Venda.query().get()
        self.assertIsNotNone(saved_venda)
        self.assertEquals(Decimal('1.01'), saved_venda.preco)

    def test_error(self):
        template_response = save()
        errors = template_response.context['errors']
        self.assertSetEqual(set(['preco']), set(errors.keys()))
        self.assert_can_render(template_response)
