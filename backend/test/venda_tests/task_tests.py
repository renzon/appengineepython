# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from decimal import Decimal
from google.appengine.ext import ndb
from base import GAETestCase
from mock import patch, Mock
from routes.vendas.tasks import contabilizar
from venda_app.venda_model import Venda, CONTABILIZADA, NOVA


class ContabilizarTests(GAETestCase):
    @patch('routes.vendas.tasks.TaskQueueCommand')
    def test_contabilizar(self, TaskQueueCommandClassMock):
        # Setando banco de dados
        Venda(preco=Decimal('0.99'), status=CONTABILIZADA).put()
        vendas_novas = [Venda(preco=Decimal('0.99'), status=NOVA),
                        Venda(preco=Decimal('1.99'), status=NOVA)]
        vendas_chaves = ndb.put_multi(vendas_novas)

        # Criação de Mock para objeto do Tipos TaskQueueCommand
        cmd = Mock()

        subtotais = {'i': 1, 1: '0.99', 2: '2.98'}

        def _contabilizar():
            params = TaskQueueCommandClassMock.call_args[1]['params']
            subtotal = params['total']
            execucao = subtotais['i']
            self.assertEqual(subtotais[execucao], subtotal)
            subtotais['i'] = execucao + 1
            contabilizar(subtotal,
                         params['cursor'])

        cmd.side_effect = _contabilizar

        TaskQueueCommandClassMock.return_value = cmd

        # Executanto handler sob teste
        contabilizar()

        # Asserções
        vendas_novas = ndb.get_multi(vendas_chaves)
        vendas_status = [v.status for v in vendas_novas]
        self.assertListEqual([CONTABILIZADA, CONTABILIZADA], vendas_status)
        self.assertEqual(2, cmd.call_count)

