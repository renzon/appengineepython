# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from gaecookie.decorator import no_csrf


# Classes de Modelo
from livro_app.livro_commands import ListarLivrosPorTituloComAutor, LivroForm, BuscarLivroPorIdCmd, AtualizarLivroCmd, \
    ApagarLivroCmd, SalvarLivroCmd, SalvarLivroComAutor
from tekton import router
from tekton.gae.middleware.redirect import RedirectResponse







# Handlers de requisições HTTP

@no_csrf
def index():
    listar_livros_cmd = ListarLivrosPorTituloComAutor()
    livro_form = LivroForm()
    livros_dcts = []
    for livro in listar_livros_cmd():
        dct = livro_form.fill_with_model(livro)
        dct['form_edicao_path'] = router.to_path(form_edicao, dct['id'])
        dct['deletar_path'] = router.to_path(deletar, dct['id'])
        dct['autor'] = livro.autor
        livros_dcts.append(dct)
    context = {'livros': livros_dcts, 'livro_form_path': router.to_path(form)}
    return TemplateResponse(context)


@no_csrf
def form_edicao(livro_id):
    buscar_livro_cmd = BuscarLivroPorIdCmd(livro_id)
    livro = buscar_livro_cmd()
    livro_form = LivroForm()
    livro_dct = livro_form.fill_with_model(livro)
    contexto = {'salvar_path': router.to_path(editar, livro_id),
                'livro': livro_dct}
    return TemplateResponse(contexto, 'livros/form.html')


def editar(livro_id, **propriedades):
    atualizar_livro_cmd = AtualizarLivroCmd(livro_id, **propriedades)
    try:
        atualizar_livro_cmd()
        return RedirectResponse(router.to_path(index))
    except CommandExecutionException:
        contexto = {'salvar_path': router.to_path(editar),
                    'erros': atualizar_livro_cmd.errors,
                    'livro': propriedades}
        return TemplateResponse(contexto, 'livros/form.html')


def deletar(livro_id):
    apagar_livro_cmd = ApagarLivroCmd(livro_id)
    apagar_livro_cmd()
    return RedirectResponse(router.to_path(index))


@no_csrf
def form():
    contexto = {'salvar_path': router.to_path(salvar)}
    return TemplateResponse(contexto)


def salvar(_logged_user, **propriedades):
    salvar_livro_cmd = SalvarLivroCmd(**propriedades)
    salvar_livro_com_autor = SalvarLivroComAutor(_logged_user, salvar_livro_cmd)
    try:
        salvar_livro_com_autor()
        return RedirectResponse(router.to_path(index))
    except CommandExecutionException:
        contexto = {'salvar_path': router.to_path(salvar),
                    'erros': salvar_livro_cmd.errors,
                    'livro': propriedades}
        return TemplateResponse(contexto, 'livros/form.html')


