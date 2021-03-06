# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
import logging
from google.appengine.api import urlfetch
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandParallel
from gaebusiness.gaeutil import UrlFetchCommand
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from tekton.router import to_path


@login_not_required
@no_csrf
def index(usuario='renzon'):
    url_base = 'https://api.github.com/users'
    url_usuario = to_path(url_base, usuario)
    url_repos = to_path(url_usuario, 'repos')
    headers = {'Accept': 'application/vnd.github.v3+json'}
    cmd_usuario = UrlFetchCommand(url_usuario, headers=headers)
    cmd_repos = UrlFetchCommand(url_repos, headers=headers)
    CommandParallel(cmd_usuario, cmd_repos).execute()
    resultado_usuario = cmd_usuario.result
    resultado_repos = cmd_repos.result
    usuario_dct = json.loads(resultado_usuario.content)
    repos_list = json.loads(resultado_repos.content)
    if len(repos_list) > 7:
        repos_list = repos_list[:7]
    logging.info(repr(repos_list))
    contexto = {'usuario': usuario,
                'avatar': usuario_dct['avatar_url'],
                'repos': repos_list}
    return TemplateResponse(contexto, 'github.html')
