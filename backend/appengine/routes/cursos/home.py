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
    cmd = curso_facade.list_cursos_cmd()
    cursos = cmd()
    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    curso_form = curso_facade.curso_form()

    def localize_curso(curso):
        curso_dct = curso_form.fill_with_model(curso)
        curso_dct['edit_path'] = router.to_path(edit_path, curso_dct['id'])
        curso_dct['delete_path'] = router.to_path(delete_path, curso_dct['id'])
        return curso_dct

    localized_cursos = [localize_curso(curso) for curso in cursos]
    context = {'cursos': localized_cursos,
               'salvar_path': router.to_path(rest.new),
               'editar_path': router.to_path(rest.edit),
               'listar_path': router.to_path(rest.index)}
    return TemplateResponse(context, 'cursos/curso_home.html')


def delete(curso_id):
    curso_facade.delete_curso_cmd(curso_id)()
    return RedirectResponse(router.to_path(index))

