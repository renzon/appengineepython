# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandParallel
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand, SingleModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode
from venda_app.venda_model import Venda, NOVA, CONTABILIZADA


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


class BuscarVendaPorStatus(SingleModelSearchCommand):
    def __init__(self, status, start_cursor=None, offset=0, use_cache=False):
        super(BuscarVendaPorStatus, self).__init__(Venda.query_por_status_ordenado_por_data(status), start_cursor,
                                                   offset, use_cache)


class ContabilizarVenda(CommandParallel):
    def __init__(self, start_cursor=None):
        self._busca_cmd = BuscarVendaPorStatus(NOVA, start_cursor)
        super(ContabilizarVenda, self).__init__(self._busca_cmd)
        self.cursor = None

    def do_business(self):
        super(ContabilizarVenda, self).do_business()
        venda = self._busca_cmd.result
        self.cursor = self._busca_cmd.cursor
        if venda:
            venda.status = CONTABILIZADA
            self._to_commit = venda

