# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from decimal import Decimal
from google.appengine.ext import ndb
from base import GAETestCase
from routes.vendas.tasks import contabilizar
from venda_app.venda_model import Venda, CONTABILIZADA, NOVA


class ContabilizarTests(GAETestCase):
    def test_contabilizar(self):
        Venda(preco=Decimal('0.99'), status=CONTABILIZADA).put()
        vendas_novas = [Venda(preco=Decimal('0.99'), status=NOVA),
                        Venda(preco=Decimal('1.99'), status=NOVA)]
        vendas_chaves = ndb.put_multi(vendas_novas)
        contabilizar()
        vendas_novas = ndb.get_multi(vendas_chaves)
        vendas_status = [v.status for v in vendas_novas]
        self.assertListEqual([CONTABILIZADA, CONTABILIZADA],
                             vendas_status)
