# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaegraph.business_base import NodeSearch, DeleteNode
from curso_app.curso_commands import ListCursoCommand, SaveCursoCommand, UpdateCursoCommand, CursoForm,\
    GetCursoCommand, DeleteCursoCommand


def save_curso_cmd(**curso_properties):
    """
    Command to save Curso entity
    :param curso_properties: a dict of properties to save on model
    :return: a Command that save Curso, validating and localizing properties received as strings
    """
    return SaveCursoCommand(**curso_properties)


def update_curso_cmd(curso_id, **curso_properties):
    """
    Command to update Curso entity with id equals 'curso_id'
    :param curso_properties: a dict of properties to update model
    :return: a Command that update Curso, validating and localizing properties received as strings
    """
    return UpdateCursoCommand(curso_id, **curso_properties)


def list_cursos_cmd():
    """
    Command to list Curso entities ordered by their creation dates
    :return: a Command proceed the db operations when executed
    """
    return ListCursoCommand()


def curso_form(**kwargs):
    """
    Function to get Curso's detail form.
    :param kwargs: form properties
    :return: Form
    """
    return CursoForm(**kwargs)


def get_curso_cmd(curso_id):
    """
    Find curso by her id
    :param curso_id: the curso id
    :return: Command
    """
    return GetCursoCommand(curso_id)



def delete_curso_cmd(curso_id):
    """
    Construct a command to delete a Curso
    :param curso_id: curso's id
    :return: Command
    """
    return DeleteCursoCommand(curso_id)

