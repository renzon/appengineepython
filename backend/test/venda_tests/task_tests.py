# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from decimal import Decimal
from google.appengine.ext import ndb
from base import GAETestCase
from mock import patch, Mock
from routes.vendas.tasks import contabilizar
from venda_app.venda_model import Venda, CONTABILIZADA, NOVA


class ContabilizarTests(GAETestCase):
    @patch('routes.vendas.tasks')
    def test_contabilizar(self, TaskQueueCommandClassMock):
        Venda(preco=Decimal('0.99'), status=CONTABILIZADA).put()
        vendas_novas = [Venda(preco=Decimal('0.99'), status=NOVA),
                        Venda(preco=Decimal('1.99'), status=NOVA)]
        vendas_chaves = ndb.put_multi(vendas_novas)
        cmd = Mock()

        def cmd_init(queue, path, params):
            cmd.reset_mock()

            def _contabilizar():
                contabilizar(params['total'], params['cursor'])

            cmd.__call__ = _contabilizar
            return cmd

        TaskQueueCommandClassMock.__call__ = cmd_init
        contabilizar()

        vendas_novas = ndb.get_multi(vendas_chaves)
        vendas_status = [v.status for v in vendas_novas]
        self.assertListEqual([CONTABILIZADA, CONTABILIZADA],
                             vendas_status)
