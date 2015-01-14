# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from tekton.gae.middleware.json_middleware import JsonResponse
from curso_app import curso_facade


def index():
    cmd = curso_facade.list_cursos_cmd()
    curso_list = cmd()
    curso_form = curso_facade.curso_form()
    curso_dcts = [curso_form.fill_with_model(m) for m in curso_list]
    return JsonResponse(curso_dcts)


def new(_resp, **curso_properties):
    cmd = curso_facade.save_curso_cmd(**curso_properties)
    return _save_or_update_json_response(cmd, _resp)


def edit(_resp, id, **curso_properties):
    cmd = curso_facade.update_curso_cmd(id, **curso_properties)
    return _save_or_update_json_response(cmd, _resp)


def delete(_resp, id):
    cmd = curso_facade.delete_curso_cmd(id)
    try:
        cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)


def _save_or_update_json_response(cmd, _resp):
    try:
        curso = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    curso_form = curso_facade.curso_form()
    return JsonResponse(curso_form.fill_with_model(curso))

