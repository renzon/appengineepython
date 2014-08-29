# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaecookie.decorator import no_csrf
from gaepermission.decorator import permissions
from config.template_middleware import TemplateResponse
from permission_app.model import ADMIN, GERENTE


@permissions(ADMIN, GERENTE)
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

