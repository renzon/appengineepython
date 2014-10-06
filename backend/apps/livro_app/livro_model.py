# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaeforms.ndb.property import SimpleCurrency
from gaegraph.model import Node, Arc


class Livro(Node):
    titulo = ndb.StringProperty(required=True)
    preco = SimpleCurrency(required=True)
    lancamento = ndb.DateProperty()

    @classmethod
    def query_listar_livros_ordenados_por_titulo(cls):
        return cls.query().order(Livro.titulo)


class AutorArco(Arc):
    origin = ndb.KeyProperty(Node)  # Chave que irá referenciar o usuário
    destination = ndb.KeyProperty(Livro)  # Chave que irá referenciar o livro
