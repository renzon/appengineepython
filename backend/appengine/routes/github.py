# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
from google.appengine.api import urlfetch
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from tekton.router import to_path


@login_not_required
@no_csrf
def index(usuario='renzon'):
    url_base = 'https://api.github.com/users'
    url_usuario = to_path(url_base, usuario)
    headers = {'Accept': 'application/vnd.github.v3+json'}
    resultado = urlfetch.fetch(url=url_usuario, headers=headers)
    usuario_dct = json.loads(resultado.content)
    contexto = {'usuario': usuario,
                'avatar': usuario_dct['avatar_url']}
    return TemplateResponse(contexto, 'github.html')
