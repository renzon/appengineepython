# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from venda_app.venda_model import Venda
from routes.vendas.home import index, delete
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Venda)
        template_response = index()
        self.assert_can_render(template_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        venda = mommy.save_one(Venda)
        redirect_response = delete(venda.key.id())
        self.assertIsInstance(redirect_response, RedirectResponse)
        self.assertIsNone(venda.key.get())

