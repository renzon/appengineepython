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
def ola(_resp, nome, sobrenome):
    _resp.write("Olá %s %s" % (nome, sobrenome))
