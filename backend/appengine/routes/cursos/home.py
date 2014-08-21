# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from tekton import router
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from curso_app import facade
from routes.cursos import admin


@login_not_required
@no_csrf
def index():
    cmd = facade.list_cursos_cmd()
    cursos = cmd()
    public_form = facade.curso_public_form()
    curso_public_dcts = [public_form.fill_with_model(curso) for curso in cursos]
    context = {'cursos': curso_public_dcts,'admin_path':router.to_path(admin)}
    return TemplateResponse(context)

