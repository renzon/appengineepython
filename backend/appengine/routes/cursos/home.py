# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from tekton import router
from gaecookie.decorator import no_csrf
from curso_app import curso_facade
from routes.cursos import new, edit, rest
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index():
    context = {'salvar_path': router.to_path(rest.new),
               'editar_path': router.to_path(rest.edit),
               'apagar_path': router.to_path(rest.delete),
               'listar_path': router.to_path(rest.index)}
    return TemplateResponse(context, 'cursos/curso_home.html')


def delete(curso_id):
    curso_facade.delete_curso_cmd(curso_id)()
    return RedirectResponse(router.to_path(index))

