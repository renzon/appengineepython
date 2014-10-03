# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from itertools import izip

from google.appengine.ext import ndb

from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaeforms.ndb.form import ModelForm
from gaegraph.model import Node, Arc
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


class AutorArco(Arc):
    origin = ndb.KeyProperty(Node)  # Chave que irá referenciar o usuário
    destination = ndb.KeyProperty(Livro)  # Chave que irá referenciar o livro


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


def deletar(livro_id):
    livro_chave = ndb.Key(Livro, int(livro_id))
    query = AutorArco.find_origins(livro_chave)
    chaves_a_serem_apagadas = query.fetch(keys_only=True)
    chaves_a_serem_apagadas.append(livro_chave)
    ndb.delete_multi(chaves_a_serem_apagadas)
    return RedirectResponse(router.to_path(index))


@no_csrf
def index():
    livros = Livro.query_listar_livros_ordenados_por_titulo().fetch()
    autores_queries = [AutorArco.find_origins(livro) for livro in livros]
    autores_arcos_futures = [q.get_async() for q in autores_queries]  # Tempo igual ao tempo de uma busca
    autores_arcos = [arco_future.get_result() for arco_future in autores_arcos_futures]
    autores_keys = [arco.origin for arco in autores_arcos]
    autores = ndb.get_multi(autores_keys)
    livro_form = LivroForm()
    livros_dcts = [livro_form.fill_with_model(livro) for livro in livros]
    for livro, autor in izip(livros_dcts, autores):
        livro['form_edicao_path'] = router.to_path(form_edicao, livro['id'])
        livro['deletar_path'] = router.to_path(deletar, livro['id'])
        livro['autor'] = autor
    context = {'livros': livros_dcts, 'livro_form_path': router.to_path(form)}
    return TemplateResponse(context)


@no_csrf
def form():
    contexto = {'salvar_path': router.to_path(salvar)}
    return TemplateResponse(contexto)


def salvar(_logged_user, **propriedades):
    livro_form = LivroForm(**propriedades)
    erros = livro_form.validate()
    if erros:
        contexto = {'salvar_path': router.to_path(salvar),
                    'erros': erros,
                    'livro': propriedades}
        return TemplateResponse(contexto, 'livros/form.html')
    livro = livro_form.fill_model()
    chave_do_livro = livro.put()
    autor_arco = AutorArco(origin=_logged_user.key, destination=chave_do_livro)
    autor_arco.put()
    return RedirectResponse(router.to_path(index))