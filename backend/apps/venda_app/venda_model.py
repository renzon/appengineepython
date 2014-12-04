# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from google.appengine.ext.db import StringProperty
from gaegraph.model import Node
from gaeforms.ndb import property

NOVA = 'NOVA'
CONTABILIZADA = 'CONTABILIZADA'


class Venda(Node):
    preco = property.SimpleCurrency(required=True)
    status = StringProperty(default=NOVA, choices=[NOVA, CONTABILIZADA])

