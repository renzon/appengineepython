# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from curso_app import curso_facade
from routes import cursos
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index(curso_id):
    curso = curso_facade.get_curso_cmd(curso_id)()
    curso_form = curso_facade.curso_form()
    context = {'save_path': router.to_path(save, curso_id), 'curso': curso_form.fill_with_model(curso)}
    return TemplateResponse(context, 'cursos/curso_form.html')


def save(curso_id, **curso_properties):
    cmd = curso_facade.update_curso_cmd(curso_id, **curso_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors, 'curso': curso_properties}

        return TemplateResponse(context, 'cursos/curso_form.html')
    return RedirectResponse(router.to_path(cursos))

