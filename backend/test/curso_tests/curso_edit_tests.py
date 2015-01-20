# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from curso_app.curso_model import Curso
from routes.cursos.edit import index, save
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        curso = mommy.save_one(Curso)
        template_response = index(curso.key.id())
        self.assert_can_render(template_response)


class EditTests(GAETestCase):
    def test_success(self):
        curso = mommy.save_one(Curso)
        old_properties = curso.to_dict()
        redirect_response = save(curso.key.id(), preco='1.01', nome='nome_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        edited_curso = curso.key.get()
        self.assertEquals(Decimal('1.01'), edited_curso.preco)
        self.assertEquals('nome_string', edited_curso.nome)
        self.assertNotEqual(old_properties, edited_curso.to_dict())

    def test_error(self):
        curso = mommy.save_one(Curso)
        old_properties = curso.to_dict()
        template_response = save(curso.key.id())
        errors = template_response.context['errors']
        self.assertSetEqual(set(['preco', 'nome']), set(errors.keys()))
        self.assertEqual(old_properties, curso.key.get().to_dict())
        self.assert_can_render(template_response)
