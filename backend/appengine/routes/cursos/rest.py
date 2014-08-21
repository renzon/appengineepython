# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from tekton.gae.middleware.json_middleware import JsonResponse
from curso_app import facade


def index():
    cmd = facade.list_cursos_cmd()
    curso_list = cmd()
    short_form=facade.curso_short_form()
    curso_short = [short_form.fill_with_model(m) for m in curso_list]
    return JsonResponse(curso_short)


def save(**curso_properties):
    cmd = facade.save_curso_cmd(**curso_properties)
    return _save_or_update_json_response(cmd)


def update(curso_id, **curso_properties):
    cmd = facade.update_curso_cmd(curso_id, **curso_properties)
    return _save_or_update_json_response(cmd)


def delete(curso_id):
    facade.delete_curso_cmd(curso_id)()


def _save_or_update_json_response(cmd):
    try:
        curso = cmd()
    except CommandExecutionException:
        return JsonResponse({'errors': cmd.errors})
    short_form=facade.curso_short_form()
    return JsonResponse(short_form.fill_with_model(curso))

