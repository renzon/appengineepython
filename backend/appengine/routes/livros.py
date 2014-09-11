# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from decimal import Decimal

from google.appengine.ext import ndb
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaeforms import base
from gaegraph.model import Node
from gaeforms.ndb import property

# Classes de Modelo
from tekton import router


class Livro(Node):
    titulo = ndb.StringProperty(required=True)
    preco = property.SimpleCurrency(required=True)
    lancamento = ndb.DateProperty()


# Formulários

class LivroForm(base.Form):
    titulo = base.StringField(required=True)
    preco = base.DecimalField(required=True, lower=0)
    lancamento = base.DateField()


# Handler de requisições HTTP
@no_csrf
def form():
    contexto = {'salvar_path': router.to_path(salvar)}
    return TemplateResponse(contexto)


def salvar(**propriedades):
    livro_form = LivroForm(**propriedades)
    erros = livro_form.validate()
    if erros:
        contexto = {'salvar_path': router.to_path(salvar),
                    'erros': erros,
                    'livro': propriedades}
        return TemplateResponse(contexto, 'livros/form.html')
    propriedades_transformadas = livro_form.normalize()
    livro = Livro(**propriedades_transformadas)
    livro.put()