# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from google.appengine.ext import ndb

from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaeforms.ndb.form import ModelForm
from gaegraph.model import Node
from gaeforms.ndb import property


# Classes de Modelo
from tekton import router
from tekton.gae.middleware.redirect import RedirectResponse


class Livro(Node):
    titulo = ndb.StringProperty(required=True)
    preco = property.SimpleCurrency(required=True)
    lancamento = ndb.DateProperty()


# Formulários

class LivroForm(ModelForm):
    _model_class = Livro
    _include = [Livro.titulo, Livro.preco, Livro.lancamento]


# Handler de requisições HTTP
@no_csrf
def index():
    query = Livro.query().order(Livro.titulo)
    livros = query.fetch()
    livro_form = LivroForm()
    livros_dcts = [livro_form.fill_with_model(livro) for livro in livros]
    context = {'livros': livros_dcts, 'livro_form_path': router.to_path(form)}
    return TemplateResponse(context)


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
    livro = livro_form.fill_model()
    livro.put()
    return RedirectResponse(router.to_path(index))