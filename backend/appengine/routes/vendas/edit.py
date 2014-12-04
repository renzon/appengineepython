# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from venda_app import venda_facade
from routes import vendas
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index(venda_id):
    venda = venda_facade.get_venda_cmd(venda_id)()
    venda_form = venda_facade.venda_form()
    context = {'save_path': router.to_path(save, venda_id), 'venda': venda_form.fill_with_model(venda)}
    return TemplateResponse(context, 'vendas/venda_form.html')


def save(venda_id, **venda_properties):
    cmd = venda_facade.update_venda_cmd(venda_id, **venda_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors, 'venda': venda_properties}

        return TemplateResponse(context, 'vendas/venda_form.html')
    return RedirectResponse(router.to_path(vendas))

