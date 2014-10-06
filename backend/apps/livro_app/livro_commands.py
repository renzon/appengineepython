# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Formulários
from itertools import izip
from gaebusiness.business import CommandSequential, CommandParallel
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import DeleteArcs, DeleteNode, NodeSearch, UpdateNode, CreateSingleOriginArc, \
    SingleOriginSearch
from livro_app.livro_model import Livro, AutorArco


class LivroForm(ModelForm):
    _model_class = Livro
    _include = [Livro.titulo, Livro.preco, Livro.lancamento]


# Comandos
class ApagarAutorArcoCmd(DeleteArcs):
    def __init__(self, livro):
        super(ApagarAutorArcoCmd, self).__init__(AutorArco, destination=livro)


class ApagarLivroCmd(CommandParallel):
    def __init__(self, livro):
        delete_cmd = DeleteNode(livro)
        apagar_autor_arco_cmd = ApagarAutorArcoCmd(livro)
        super(ApagarLivroCmd, self).__init__(delete_cmd, apagar_autor_arco_cmd)


class BuscarLivroPorIdCmd(NodeSearch):
    _model_class = Livro


class SalvarLivroCmd(SaveCommand):
    _model_form_class = LivroForm


class AtualizarLivroCmd(UpdateNode):
    _model_form_class = LivroForm


class SalvarLivroComAutor(CreateSingleOriginArc):
    def __init__(self, origin, destination):
        super(SalvarLivroComAutor, self).__init__(AutorArco, origin, destination)


class ListarLivrosOrdenadosPorTituloCmd(ModelSearchCommand):
    def __init__(self):
        super(ListarLivrosOrdenadosPorTituloCmd, self).__init__(Livro.query_listar_livros_ordenados_por_titulo())


class BuscarAutor(SingleOriginSearch):
    def __init__(self, livro):
        super(BuscarAutor, self).__init__(AutorArco, livro)


class BuscarAutoresCmd(CommandParallel):
    def __init__(self, *livros):
        autores_cmds = [BuscarAutor(livro) for livro in livros]
        super(BuscarAutoresCmd, self).__init__(*autores_cmds)

    def handle_previous(self, command):
        autores_cmds = [BuscarAutor(livro) for livro in command.result]
        self.extend(autores_cmds)

    def do_business(self):
        super(BuscarAutoresCmd, self).do_business()
        self.result = [cmd.result for cmd in self]


class ListarLivrosPorTituloComAutor(CommandSequential):
    def __init__(self):
        self.__listar_livros_cmd = ListarLivrosOrdenadosPorTituloCmd()
        self.__buscar_autores_cmd = BuscarAutoresCmd()
        super(ListarLivrosPorTituloComAutor, self).__init__(self.__listar_livros_cmd,
                                                            self.__buscar_autores_cmd)

    def do_business(self):
        super(ListarLivrosPorTituloComAutor, self).do_business()
        # Iterar nos livros e acrescentar seus autores
        for livro, autor in izip(self.__listar_livros_cmd.result, self.__buscar_autores_cmd.result):
            livro.autor = autor
        self.result = self.__listar_livros_cmd.result