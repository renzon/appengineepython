# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from google.appengine.ext import ndb
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaegraph.model import Node
from gaeforms.ndb import property

# Classes de Modelo

class Livro(Node):
    titulo = ndb.StringProperty(required=True)
    preco = property.SimpleCurrency(required=True)
    lancamento = ndb.DateProperty(auto_now_add=True)


# Handler de requisições HTTP
@no_csrf
def form():
    return TemplateResponse()