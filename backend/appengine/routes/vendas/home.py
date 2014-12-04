# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from tekton import router
from gaecookie.decorator import no_csrf
from venda_app import venda_facade
from routes.vendas import new, edit
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index():
    cmd = venda_facade.list_vendas_cmd()
    vendas = cmd()
    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    venda_form = venda_facade.venda_form()

    def localize_venda(venda):
        venda_dct = venda_form.fill_with_model(venda)
        venda_dct['edit_path'] = router.to_path(edit_path, venda_dct['id'])
        venda_dct['delete_path'] = router.to_path(delete_path, venda_dct['id'])
        return venda_dct

    localized_vendas = [localize_venda(venda) for venda in vendas]
    context = {'vendas': localized_vendas,
               'new_path': router.to_path(new)}
    return TemplateResponse(context, 'vendas/venda_home.html')


def delete(venda_id):
    venda_facade.delete_venda_cmd(venda_id)()
    return RedirectResponse(router.to_path(index))

