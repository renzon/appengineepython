# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from curso_app import facade
from routes.cursos import admin


@no_csrf
def index():
    return TemplateResponse({'save_path': router.to_path(save)},'cursos/admin/form.html')


def save(_handler, curso_id=None, **curso_properties):
    cmd = facade.save_curso_cmd(**curso_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'curso': cmd.form}

        return TemplateResponse(context, 'cursos/admin/form.html')
    _handler.redirect(router.to_path(admin))

