# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from livro_app.livro_commands import ListarLivrosOrdenadosPorTituloCmd, ListarLivrosPorTituloComAutor, LivroForm, \
    BuscarLivroPorIdCmd, SalvarLivroCmd, SalvarLivroComAutor, AtualizarLivroCmd, ApagarLivroCmd


def listar_livros_por_titulo_com_autor_cmd():
    """
    Retorna comando que lista lívros ordenados por seus títulos em ordem crescente.
    Cada autor de livro também é pesquisado, ficando disponível no atributo "autor" do livro.
    :return: Comando que retorna livros quando executado
    """
    return ListarLivrosPorTituloComAutor()


def livro_form(**propriedades):
    return LivroForm(**propriedades)


def buscar_livro_por_id_cmd(livro_id):
    return BuscarLivroPorIdCmd(livro_id)


def salvar_livro_cmd(**propriedades):
    return SalvarLivroCmd(**propriedades)


def salvar_livro_com_autor_cmd(autor, salvar_livro_cmd):
    return SalvarLivroComAutor(autor, salvar_livro_cmd)


def atualizar_livro_cmd(livro_id, **propriedades):
    return AtualizarLivroCmd(livro_id, **propriedades)


def apagar_livro_cmd(livro_id):
    return ApagarLivroCmd(livro_id)