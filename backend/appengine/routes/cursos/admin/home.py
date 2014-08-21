# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from tekton import router
from gaecookie.decorator import no_csrf
from curso_app import facade
from routes.cursos.admin import new, edit


def delete(_handler, curso_id):
    facade.delete_curso_cmd(curso_id)()
    _handler.redirect(router.to_path(index))


@no_csrf
def index():
    cmd = facade.list_cursos_cmd()
    cursos = cmd()
    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    short_form = facade.curso_short_form()

    def short_curso_dict(curso):
        curso_dct = short_form.fill_with_model(curso)
        curso_dct['edit_path'] = router.to_path(edit_path, curso_dct['id'])
        curso_dct['delete_path'] = router.to_path(delete_path, curso_dct['id'])
        return curso_dct

    short_cursos = [short_curso_dict(curso) for curso in cursos]
    context = {'cursos': short_cursos,
               'new_path': router.to_path(new)}
    return TemplateResponse(context)

