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

    @classmethod
    def query_listar_livros_ordenados_por_titulo(cls):
        return cls.query().order(Livro.titulo)


# Formulários

class LivroForm(ModelForm):
    _model_class = Livro
    _include = [Livro.titulo, Livro.preco, Livro.lancamento]


# Handler de requisições HTTP

@no_csrf
def form_edicao(livro_id):
    livro_id = int(livro_id)
    livro = Livro.get_by_id(livro_id)
    livro_form = LivroForm()
    livro_dct = livro_form.fill_with_model(livro)
    contexto = {'salvar_path': router.to_path(editar, livro_id),
                'livro': livro_dct}
    return TemplateResponse(contexto, 'livros/form.html')


def editar(livro_id, **propriedades):
    livro_form = LivroForm(**propriedades)
    erros = livro_form.validate()
    if erros:
        contexto = {'salvar_path': router.to_path(editar, livro_id),
                    'erros': erros,
                    'livro': propriedades}
        return TemplateResponse(contexto, 'livros/form.html')
    livro = Livro.get_by_id(int(livro_id))
    livro_form.fill_model(livro)
    livro.put()
    return RedirectResponse(router.to_path(index))


@no_csrf
def index():
    query = Livro.query_listar_livros_ordenados_por_titulo()
    livros = query.fetch()
    livro_form = LivroForm()
    livros_dcts = [livro_form.fill_with_model(livro) for livro in livros]
    for livro in livros_dcts:
        livro['form_edicao_path'] = router.to_path(form_edicao, livro['id'])
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