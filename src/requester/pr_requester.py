import re

import requests

from src.requester.requester import Requester


class PrRequester(Requester):
    URL = 'http://www.transparencia.pr.gov.br/pte/pessoal/servidores/poderexecutivo/remuneracao'

    def __init__(self, instituicao: str = 'TODAS', cargo: str = 'TODOS', municipio: str = 'TODOS', quadro_funcional: str = 'TODOS'):
        self.instituicao = instituicao
        self.cargo = cargo
        self.municipio = municipio
        self.quadro_funcional = quadro_funcional
        self.status_code = '200'
        self.dataTableServidores_first = 0
        self.window_id = ''
        self.jsessionid = ''
        self.get_next()
        # self.STARTED = False

    def get_next(self):
        self.get_html()
        self.VIEWSTATE = re.search(r'ViewState:0"><!\[CDATA\[(.*?)]]>', self.PAGE).group(1)
        if not self.STARTED:
            self.jsessionid = re.search(r';jsessionid=(.*?)\?', self.PAGE).group(1)
            self.window_id = re.search(r'\?windowId=(.*?)"', self.PAGE).group(1)
            self.STARTED = True
        return self.PAGE

    def get_html(self) -> None:
        cookies = dict()
        data = dict()
        headers = dict()
        headers.update(self.HEADERS)
        url = ''
        if self.STARTED:
            data.update(
                {
                    'javax.faces.partial.ajax': "true",
                    'javax.faces.source': "formRemuneracoes:dataTableServidores",
                    'javax.faces.partial.execute': "formRemuneracoes:dataTableServidores",
                    'javax.faces.partial.render': "formRemuneracoes:dataTableServidores",
                    'javax.faces.behavior.event': "page",
                    'javax.faces.partial.event': "page",
                    'formRemuneracoes:dataTableServidores_pagination': "true",
                    'formRemuneracoes:dataTableServidores_first': self.dataTableServidores_first,
                    'formRemuneracoes:dataTableServidores_rows': "30",
                    'formRemuneracoes:dataTableServidores_encodeFeature': "true",
                    'formRemuneracoes': "formRemuneracoes",
                    'javax.faces.ViewState': self.VIEWSTATE,
                    'formRemuneracoes:filtroNome': "",
                    'formRemuneracoes:filtroInstituicao_focus': "",
                    'formRemuneracoes:filtroInstituicao_input': "",
                    'formRemuneracoes:filtroInstituicao_editableInput': "",
                    'formRemuneracoes:filtroCargo_focus': "",
                    'formRemuneracoes:filtroCargo_input': '',
                    'formRemuneracoes:filtroCargo_editableInput':  '',
                    'formRemuneracoes:filtroMunicipio_focus': "",
                    'formRemuneracoes:filtroMunicipio_input': "",
                    'formRemuneracoes:filtroMunicipio_editableInput': '',
                    'formRemuneracoes:filtroQuadroFuncional_focus': "",
                    'formRemuneracoes:filtroQuadroFuncional_input': "",
                    'formRemuneracoes:filtroQuadroFuncional_editableInput': '',
                    'formRemuneracoes:customRadio': "false"
                }
            )
            cookies.update(
                {
                    'JSESSIONID': self.jsessionid,
                    'ROUTEID': '.jboss'
                }
            )
            url = self.URL + '?windowId=' + self.window_id
            headers.update(
                {
                    'Accept': 'application/xml, text/xml, */*; q=0.01',
                    'Referer': url,
                    'Faces-Request': 'partial/ajax',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Cookie': 'JSESSIONID='+self.jsessionid+'; ROUTEID=.jboss',
                    'DNT': '1'
                }
            )
            self.dataTableServidores_first = self.dataTableServidores_first + 30
        else:
            data.update(
                {
                    'javax.faces.source': 'formRemuneracoes:buttonPesquisar',
                    'javax.faces.partial.execute': 'formRemuneracoes',
                    'javax.faces.partial.render': 'formRemuneracoes',
                    'javax.faces.partial.ajax': 'true',
                    'formRemuneracoes:buttonPesquisar': 'formRemuneracoes:buttonPesquisar',
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
                    'formRemuneracoes:customRadio': 'false'
                }
            )
            # self.STARTED = True
            url = self.URL

        r = requests.post(url, data=data, headers=headers, cookies=cookies)
        self.PAGE = r.text
        self.status_code = r.status_code

    def has_next(self) -> bool:
        return self.status_code == 200
