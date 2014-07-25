# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required


@login_not_required
@no_csrf
def index(_resp):
    _resp.write('Página de Usuário')


@login_not_required
@no_csrf
def ola(_resp, _req, nome, sobrenome):
    _resp.write("Olá %s %s" % (nome, sobrenome))
    # Imprimindo parametros de requisição http
    _resp.write("Parametros: %s" % _req.arguments())

@login_not_required
@no_csrf
def redirecionar(_handler):
    url = r'/usuario/ola/Renzo/Nuccitelli'
    _handler.redirect(url)