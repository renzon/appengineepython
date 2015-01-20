# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime, date
from decimal import Decimal
from base import GAETestCase
from curso_app.curso_model import Curso
from routes.cursos import rest
from gaegraph.model import Node
from mock import Mock
from mommygae import mommy


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Curso)
        mommy.save_one(Curso)
        json_response = rest.index()
        context = json_response.context
        self.assertEqual(2, len(context))
        curso_dct = context[0]
        self.assertSetEqual(set(['id', 'creation', 'preco', 'nome']),
                            set(curso_dct.iterkeys()))
        self.assert_can_serialize_as_json(json_response)


class NewTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Curso.query().get())
        json_response = rest.new(None, preco='1.01', nome='nome_string')
        db_curso = Curso.query().get()
        self.assertIsNotNone(db_curso)
        self.assertEquals(Decimal('1.01'), db_curso.preco)
        self.assertEquals('nome_string', db_curso.nome)
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        resp = Mock()
        json_response = rest.new(resp)
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['preco', 'nome']), set(errors.keys()))
        self.assert_can_serialize_as_json(json_response)


class EditTests(GAETestCase):
    def test_success(self):
        curso = mommy.save_one(Curso)
        old_properties = curso.to_dict()
        json_response = rest.edit(None, curso.key.id(), preco='1.01', nome='nome_string')
        db_curso = curso.key.get()
        self.assertEquals(Decimal('1.01'), db_curso.preco)
        self.assertEquals('nome_string', db_curso.nome)
        self.assertNotEqual(old_properties, db_curso.to_dict())
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        curso = mommy.save_one(Curso)
        old_properties = curso.to_dict()
        resp = Mock()
        json_response = rest.edit(resp, curso.key.id())
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['preco', 'nome']), set(errors.keys()))
        self.assertEqual(old_properties, curso.key.get().to_dict())
        self.assert_can_serialize_as_json(json_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        curso = mommy.save_one(Curso)
        rest.delete(None, curso.key.id())
        self.assertIsNone(curso.key.get())

    def test_non_curso_deletion(self):
        non_curso = mommy.save_one(Node)
        response = Mock()
        json_response = rest.delete(response, non_curso.key.id())
        self.assertIsNotNone(non_curso.key.get())
        self.assertEqual(500, response.status_code)
        self.assert_can_serialize_as_json(json_response)

