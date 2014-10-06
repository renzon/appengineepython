# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from livro_app.livro_commands import ListarLivrosOrdenadosPorTituloCmd, ListarLivrosPorTituloComAutor


def listar_livros_por_titulo_com_autor():
    """
    Retorna comando que lista lívros ordenados por seus títulos em ordem crescente.
    Cada autor de livro também é pesquisado, ficando disponível no atributo "autor" do livro.
    :return: Comando que retorna livros quando executado
    """
    return ListarLivrosPorTituloComAutor()