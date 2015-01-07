# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime, date
from decimal import Decimal
from base import GAETestCase
from venda_app.venda_model import Venda
from routes.vendas import rest
from mock import Mock
from mommygae import mommy


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Venda)
        mommy.save_one(Venda)
        json_response = rest.index()
        context = json_response.context
        self.assertEqual(2, len(context))
        venda_dct = context[0]
        self.assertSetEqual(set(['id', 'creation', 'preco','status']), set(venda_dct.iterkeys()))
        self.assert_can_serialize_as_json(json_response)


class NewTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Venda.query().get())
        json_response = rest.new(None, preco='1.01')
        db_venda = Venda.query().get()
        self.assertIsNotNone(db_venda)
        self.assertEquals(Decimal('1.01'), db_venda.preco)
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        resp = Mock()
        json_response = rest.new(resp)
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['preco']), set(errors.keys()))
        self.assert_can_serialize_as_json(json_response)


class EditTests(GAETestCase):
    def test_success(self):
        venda = mommy.save_one(Venda)
        old_properties = venda.to_dict()
        json_response = rest.edit(None, venda.key.id(), preco='1.01')
        db_venda = venda.key.get()
        self.assertEquals(Decimal('1.01'), db_venda.preco)
        self.assertNotEqual(old_properties, db_venda.to_dict())
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        venda = mommy.save_one(Venda)
        old_properties = venda.to_dict()
        resp = Mock()
        json_response = rest.edit(resp, venda.key.id())
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['preco']), set(errors.keys()))
        self.assertEqual(old_properties, venda.key.get().to_dict())
        self.assert_can_serialize_as_json(json_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        venda = mommy.save_one(Venda)
        rest.delete(venda.key.id())
        self.assertIsNone(venda.key.get())
