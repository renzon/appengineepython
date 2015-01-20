# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from curso_app.curso_model import Curso
from routes.cursos.new import index, save
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        template_response = index()
        self.assert_can_render(template_response)


class SaveTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Curso.query().get())
        redirect_response = save(preco='1.01', nome='nome_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        saved_curso = Curso.query().get()
        self.assertIsNotNone(saved_curso)
        self.assertEquals(Decimal('1.01'), saved_curso.preco)
        self.assertEquals('nome_string', saved_curso.nome)

    def test_error(self):
        template_response = save()
        errors = template_response.context['errors']
        self.assertSetEqual(set(['preco', 'nome']), set(errors.keys()))
        self.assert_can_render(template_response)
