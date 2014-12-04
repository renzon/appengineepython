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
def index():
    return TemplateResponse({'save_path': router.to_path(save)}, 'vendas/venda_form.html')


def save(**venda_properties):
    cmd = venda_facade.save_venda_cmd(**venda_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'venda': venda_properties}

        return TemplateResponse(context, 'vendas/venda_form.html')
    return RedirectResponse(router.to_path(vendas))

