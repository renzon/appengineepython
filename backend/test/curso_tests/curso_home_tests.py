# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from curso_app.curso_model import Curso
from routes.cursos.home import index, delete
from gaebusiness.business import CommandExecutionException
from gaegraph.model import Node
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Curso)
        template_response = index()
        self.assert_can_render(template_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        curso = mommy.save_one(Curso)
        redirect_response = delete(curso.key.id())
        self.assertIsInstance(redirect_response, RedirectResponse)
        self.assertIsNone(curso.key.get())

    def test_non_curso_deletion(self):
        non_curso = mommy.save_one(Node)
        self.assertRaises(CommandExecutionException, delete, non_curso.key.id())
        self.assertIsNotNone(non_curso.key.get())

