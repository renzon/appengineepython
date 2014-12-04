# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode
from venda_app.venda_model import Venda



class VendaSaveForm(ModelForm):
    """
    Form used to save and update Venda
    """
    _model_class = Venda
    _include = [Venda.preco]


class VendaForm(ModelForm):
    """
    Form used to expose Venda's properties for list or json
    """
    _model_class = Venda




class SaveVendaCommand(SaveCommand):
    _model_form_class = VendaSaveForm


class UpdateVendaCommand(UpdateNode):
    _model_form_class = VendaSaveForm


class ListVendaCommand(ModelSearchCommand):
    def __init__(self):
        super(ListVendaCommand, self).__init__(Venda.query_by_creation())

