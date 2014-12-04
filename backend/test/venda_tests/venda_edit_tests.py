# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from venda_app.venda_model import Venda
from routes.vendas.edit import index, save
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        venda = mommy.save_one(Venda)
        template_response = index(venda.key.id())
        self.assert_can_render(template_response)


class EditTests(GAETestCase):
    def test_success(self):
        venda = mommy.save_one(Venda)
        old_properties = venda.to_dict()
        redirect_response = save(venda.key.id(), preco='1.01')
        self.assertIsInstance(redirect_response, RedirectResponse)
        edited_venda = venda.key.get()
        self.assertEquals(Decimal('1.01'), edited_venda.preco)
        self.assertNotEqual(old_properties, edited_venda.to_dict())

    def test_error(self):
        venda = mommy.save_one(Venda)
        old_properties = venda.to_dict()
        template_response = save(venda.key.id())
        errors = template_response.context['errors']
        self.assertSetEqual(set(['preco']), set(errors.keys()))
        self.assertEqual(old_properties, venda.key.get().to_dict())
        self.assert_can_render(template_response)
