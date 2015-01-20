# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from unittest.case import TestCase
from livro_app.livro_commands import BuscarLivroPorIdCmd

class BuscarLivroTests(TestCase):
    def test_livro_nao_existente(self):
        cmd = BuscarLivroPorIdCmd(1)
        livro = cmd()
        self.assertIsNone(livro)