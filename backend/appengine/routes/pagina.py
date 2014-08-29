# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required, login_required
from config.template_middleware import TemplateResponse

@login_required
@no_csrf
def index():
    class Curso(object):
        def __init__(self, nome=''):
            self.nome = nome

    cursos = [Curso(nome) for nome in ('PyPrático',
                                       'Objetos Pythônicos',
                                       'Python para quem sabe Python')]

    contexto = {'lista_cursos': cursos}
    return TemplateResponse(contexto)

