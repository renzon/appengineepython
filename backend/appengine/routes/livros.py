# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from decimal import Decimal

from google.appengine.ext import ndb
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaegraph.model import Node
from gaeforms.ndb import property

# Classes de Modelo
from tekton import router


class Livro(Node):
    titulo = ndb.StringProperty(required=True)
    preco = property.SimpleCurrency(required=True)
    lancamento = ndb.DateProperty(auto_now_add=True)


# Handler de requisições HTTP
@no_csrf
def form():
    contexto = {'salvar_path': router.to_path(salvar)}
    return TemplateResponse(contexto)


def salvar(titulo, preco, **outras_propriedades):
    preco = Decimal(preco)
    livro = Livro(titulo=titulo, preco=preco)
    livro.put()