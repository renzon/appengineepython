# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from livro_app.livro_commands import BuscarLivroPorIdCmd
from livro_app.livro_model import Livro
from mommygae import mommy


class BuscarLivroTests(GAETestCase):
    def test_livro_nao_existente(self):
        cmd = BuscarLivroPorIdCmd(1)
        livro = cmd()
        self.assertIsNone(livro)

    def test_livro_existente(self):
        livro = mommy.save_one(Livro, titulo='App Engine e Python')
        cmd = BuscarLivroPorIdCmd(livro.key.id())
        livro_do_bd = cmd()
        self.assertEqual(livro, livro_do_bd)
        self.assertEqual(livro.titulo, livro_do_bd.titulo)