import requests

from src.requester.requester import Requester


class PrRequester(Requester):
    URL = 'http://www.transparencia.pr.gov.br/pte/pessoal/servidores/poderexecutivo/remuneracao?windowId=3fc'

    def __init__(self, instituicao: str = 'TODAS', cargo: str = 'TODOS', municipio: str = 'TODOS', quadro_funcional: str = 'TODOS'):
        self.instituicao = instituicao
        self.cargo = cargo
        self.municipio = municipio
        self.quadro_funcional = quadro_funcional
        self.ViewState = '-2440845790774114559:1958432107984863730'
        self.status_code = '200'

    def get_next(self) -> None:
        self.get_html()
        # qualquer tratamento especifico

    def get_html(self) -> None:
        data = {
            'javax.faces.partial.ajax': 'true',
            'formRemuneracoes': 'formRemuneracoes',
            'formRemuneracoes:filtroNome': '',
            'formRemuneracoes:filtroInstituicao_focus': '',
            'formRemuneracoes:filtroInstituicao_input': '',
            'formRemuneracoes:filtroInstituicao_editableInput': self.instituicao,
            'formRemuneracoes:filtroCargo_focus': '',
            'formRemuneracoes:filtroCargo_input': '',
            'formRemuneracoes:filtroCargo_editableInput': self.cargo,
            'formRemuneracoes:filtroMunicipio_focus': '',
            'formRemuneracoes:filtroMunicipio_input': '',
            'formRemuneracoes:filtroMunicipio_editableInput': self.municipio,
            'formRemuneracoes:filtroQuadroFuncional_focus': '',
            'formRemuneracoes:filtroQuadroFuncional_input': '',
            'formRemuneracoes:filtroQuadroFuncional_editableInput': self.quadro_funcional,
            'formRemuneracoes:customRadio': 'false',
            'javax.faces.ViewState': self.ViewState
        }
        if not self.STARTED:
            data.update(
                {
                    'javax.faces.source': 'formRemuneracoes:buttonPesquisar',
                    'javax.faces.partial.execute': 'formRemuneracoes',
                    'javax.faces.partial.render': 'formRemuneracoes',
                    'formRemuneracoes:buttonPesquisar': 'formRemuneracoes:buttonPesquisar',
                }
            )
        else:
            data.update(
                {
                    'javax.faces.source': 'formRemuneracoes:dataTableServidores',
                    'javax.faces.partial.execute': 'formRemuneracoes:dataTableServidores',
                    'javax.faces.partial.render': 'formRemuneracoes:dataTableServidores',
                    'javax.faces.behavior.event': 'page',
                    'javax.faces.partial.event': 'page',
                    'formRemuneracoes:dataTableServidores_pagination': 'true',
                    'formRemuneracoes:dataTableServidores_first': '30',
                    'formRemuneracoes:dataTableServidores_rows': '30',
                    'formRemuneracoes:dataTableServidores_encodeFeature': 'true'
                }
            )
        r = requests.post(self.URL, data=data, headers=self.HEADERS)
        self.PAGE = r.text
        self.status_code = r.status_code

    def has_next(self) -> bool:
        return self.status_code == 200
