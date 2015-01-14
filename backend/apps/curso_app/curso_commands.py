# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode, NodeSearch, DeleteNode
from curso_app.curso_model import Curso



class CursoSaveForm(ModelForm):
    """
    Form used to save and update Curso
    """
    _model_class = Curso
    _include = [Curso.preco, 
                Curso.nome]


class CursoForm(ModelForm):
    """
    Form used to expose Curso's properties for list or json
    """
    _model_class = Curso


class GetCursoCommand(NodeSearch):
    _model_class = Curso


class DeleteCursoCommand(DeleteNode):
    _model_class = Curso


class SaveCursoCommand(SaveCommand):
    _model_form_class = CursoSaveForm


class UpdateCursoCommand(UpdateNode):
    _model_form_class = CursoSaveForm


class ListCursoCommand(ModelSearchCommand):
    def __init__(self):
        super(ListCursoCommand, self).__init__(Curso.query_by_creation())

