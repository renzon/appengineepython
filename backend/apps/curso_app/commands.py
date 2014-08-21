# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode
from curso_app.model import Curso

class CursoPublicForm(ModelForm):
    """
    Form used to show properties on app's home
    """
    _model_class = Curso
    _include = [Curso.titulo, 
                Curso.preco, 
                Curso.inicio]


class CursoForm(ModelForm):
    """
    Form used to save and update operations on app's admin page
    """
    _model_class = Curso
    _include = [Curso.titulo, 
                Curso.preco, 
                Curso.inicio]


class CursoDetailForm(ModelForm):
    """
    Form used to show entity details on app's admin page
    """
    _model_class = Curso
    _include = [Curso.titulo, 
                Curso.creation, 
                Curso.preco, 
                Curso.inicio]


class CursoShortForm(ModelForm):
    """
    Form used to show entity short version on app's admin page, mainly for tables
    """
    _model_class = Curso
    _include = [Curso.titulo, 
                Curso.creation, 
                Curso.preco, 
                Curso.inicio]


class SaveCursoCommand(SaveCommand):
    _model_form_class = CursoForm


class UpdateCursoCommand(UpdateNode):
    _model_form_class = CursoForm


class ListCursoCommand(ModelSearchCommand):
    def __init__(self):
        super(ListCursoCommand, self).__init__(Curso.query_by_creation())

