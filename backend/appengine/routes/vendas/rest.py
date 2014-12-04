# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from tekton.gae.middleware.json_middleware import JsonResponse
from venda_app import venda_facade


def index():
    cmd = venda_facade.list_vendas_cmd()
    venda_list = cmd()
    venda_form = venda_facade.venda_form()
    venda_dcts = [venda_form.fill_with_model(m) for m in venda_list]
    return JsonResponse(venda_dcts)


def new(_resp, **venda_properties):
    cmd = venda_facade.save_venda_cmd(**venda_properties)
    return _save_or_update_json_response(cmd, _resp)


def edit(_resp, id, **venda_properties):
    cmd = venda_facade.update_venda_cmd(id, **venda_properties)
    return _save_or_update_json_response(cmd, _resp)


def delete(id):
    venda_facade.delete_venda_cmd(id)()


def _save_or_update_json_response(cmd, _resp):
    try:
        venda = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    venda_form = venda_facade.venda_form()
    return JsonResponse(venda_form.fill_with_model(venda))

