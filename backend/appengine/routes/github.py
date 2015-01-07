# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.api import urlfetch
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from tekton.router import to_path


@login_not_required
@no_csrf
def index(_resp, usuario='renzon'):
    url_base = 'https://api.github.com/users'
    url_usuario = to_path(url_base, usuario)
    resultado = urlfetch.fetch(url=url_usuario)
    _resp.write(resultado.content)