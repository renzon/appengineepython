# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from livro_app.livro_commands import BuscarLivroPorIdCmd

class BuscarLivroTests(GAETestCase):
    def test_livro_nao_existente(self):
        cmd = BuscarLivroPorIdCmd(1)
        livro = cmd()
        self.assertIsNone(livro)