# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Node
from gaeforms.ndb import property

NOVA = 'NOVA'
CONTABILIZADA = 'CONTABILIZADA'


class Venda(Node):
    preco = property.SimpleCurrency(required=True)
    status = ndb.StringProperty(default=NOVA, choices=[NOVA, CONTABILIZADA])

    @classmethod
    def query_por_status_ordenado_por_data(cls, status):
        return cls.query(cls.status == status).order(cls.creation)

