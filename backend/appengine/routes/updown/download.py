# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf


@no_csrf
def index(_handler, blob_key,nome_de_arquivo):
    _handler.send_blob(blob_key)