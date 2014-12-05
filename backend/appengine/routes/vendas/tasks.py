# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import date
from decimal import Decimal

from google.appengine.api import mail

from config.template import render

from gaebusiness.gaeutil import TaskQueueCommand
from gaecookie.decorator import no_csrf
from gaeforms.base import Form, StringField, DateField, DecimalField
from gaepermission.decorator import login_not_required
import settings
from tekton.router import to_path
from venda_app.venda_facade import contabilizar_venda_cmd


@login_not_required
@no_csrf
def contabilizar(total='0.00', cursor=None):
    total = Decimal(total)
    contabilizar_cmd = contabilizar_venda_cmd(cursor)
    venda = contabilizar_cmd()
    if venda:
        total += venda.preco
        params = {'total': '%s' % total,
                  'cursor': contabilizar_cmd.cursor.urlsafe()}
        proximo_passo_path = to_path(contabilizar)
        task_cmd = TaskQueueCommand('rapida',
                                    proximo_passo_path,
                                    params=params)
        task_cmd()
    else:
        class TotalForm(Form):
            nome = StringField()
            valor = DecimalField()
            data = DateField()

        form = TotalForm()
        dados = form.localize(valor=total,
                              nome='Renzo',
                              data=date.today())
        corpo_email = render('vendas/contabilizacao.txt', dados)
        mail.send_mail(settings.SENDER_EMAIL,
                       'renzo@python.pro.br',
                       'Contabilização de Vendas',
                       corpo_email)
