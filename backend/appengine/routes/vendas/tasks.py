# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging
from decimal import Decimal
from google.appengine.api import taskqueue
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from tekton.router import to_path


@login_not_required
@no_csrf
def contabilizar(total='0.00', i='1'):
    total = Decimal(total)
    i = int(i)
    if i < 4:
        total += i
        i += 1
        params = {'total': '%s' % total,
                  'i': i}
        proximo_passo_path = to_path(contabilizar)
        taskqueue.add(url=proximo_passo_path, params=params)
    else:
        logging.info('Contabilização terminada: %s' % total)