# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from curso_app import facade
from routes.cursos import admin


@no_csrf
def index(curso_id):
    curso = facade.get_curso_cmd(curso_id)()
    detail_form = facade.curso_detail_form()
    context = {'save_path': router.to_path(save, curso_id), 'curso': detail_form.fill_with_model(curso)}
    return TemplateResponse(context, 'cursos/admin/form.html')


def save(_handler, curso_id, **curso_properties):
    cmd = facade.update_curso_cmd(curso_id, **curso_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'curso': cmd.form}

        return TemplateResponse(context, 'cursos/admin/form.html')
    _handler.redirect(router.to_path(admin))

