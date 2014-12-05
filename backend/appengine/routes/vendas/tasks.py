# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging
from decimal import Decimal
from google.appengine.api import taskqueue
from gaebusiness.gaeutil import TaskQueueCommand
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
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
        logging.info('Contabilização terminada: %s' % total)