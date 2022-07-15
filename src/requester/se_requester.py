import re
from re import Match

import requests

from src.requester.requester import Requester


class SeRequester(Requester):
    URL = 'https://www.transparencia.se.gov.br/Pessoal/PorOrgao.xhtml'
    other = 'http://www.transparencia.pr.gov.br/pte/pessoal/servidores/poderexecutivo/remuneracao;jsessionid=XwizLa1CTC6mF46NrrKzFsKL_XW6iARrT1U5t8Zf.ssecs75004?windowId=ff2'
    REGEX_ACHAR_TOTAL_SERVIDORES = r'Total de Servidores:</td><td class="ui-state-default" style="text-align:left; font-weight: bold">(.*?)</td'
    REGEX_ACHAR_VIEWSTATE_INICIAL = r'id="j_id1:javax.faces.ViewState:0" value="(.*?)"'
    REGEX_ACHAR_VIEWSTATE_NOVA = r'id="j_id1:javax.faces.ViewState:0"><!\[CDATA\[(.*?)]]'
    REGEX_ACHAR_JSESSION = r'jsessionid=(.*?)\?ln'
    REGEX_TABLE_PAGES = r'<table role="grid">(.*?)</table>'
    REGEX_TABLE_LAST_PAGE = r'<update id="frmPrincipal:Tabela"><!\[CDATA\[(.*?)]]></update>'
    TABLE_INIT_TAG = '<table role="grid">'
    TABLE_END_TAG = '</table>'
    TBODY_INIT_TAG = '<tbody id="frmPrincipal:Tabela_data">'
    TBODY_END_TAG = '</tbody>'

    def __init__(self, orgao: str = '4'):
        self.orgao = orgao
        self.status_code = '200'
        self.servidores_ja_vistos = 0
        self.window_id = ''
        self.jsessionid = ''
        self.total_servidores = 1
        r = requests.post(self.URL)
        # inicializa variáveis internas
        PAGE = r.text
        self.VIEWSTATE = re.search(self.REGEX_ACHAR_VIEWSTATE_INICIAL, PAGE).group(1)
        self.jsessionid = re.search(self.REGEX_ACHAR_JSESSION, PAGE).group(1)

    def get_next(self) -> str:
        self.get_html()

        self.VIEWSTATE = re.search(self.REGEX_ACHAR_VIEWSTATE_NOVA, self.PAGE).group(1)
        if not self.STARTED:
            total_servidores = re.search(self.REGEX_ACHAR_TOTAL_SERVIDORES, self.PAGE).group(1)
            self.total_servidores = int(total_servidores)
            self.STARTED = True
        try:
            table_content = re.search(self.REGEX_TABLE_PAGES, self.PAGE).group(1)
        except AttributeError:
            # ocorre quando o formato de resposta do servidor muda
            table_content = re.search(self.REGEX_TABLE_LAST_PAGE, self.PAGE).group(1)
            table_content = self.TBODY_INIT_TAG + table_content + self.TBODY_END_TAG
        except:
            print('Houve algum tipo de erro na extração dos dados do html')
            exit(1)
        return self.TABLE_INIT_TAG + table_content + self.TABLE_END_TAG

    def get_html(self) -> None:
        cookies = {
            'JSESSIONID': self.jsessionid,
        }
        data = dict()
        if self.STARTED:
            data.update(
                {
                    'javax.faces.partial.ajax': 'true',
                    'javax.faces.source': 'frmPrincipal:Tabela',
                    'javax.faces.partial.execute': 'frmPrincipal:Tabela',
                    'javax.faces.partial.render': 'frmPrincipal:Tabela',
                    'frmPrincipal:Tabela_pagination': "true",
                    'frmPrincipal:Tabela_first': self.servidores_ja_vistos,
                    'frmPrincipal:Tabela_rows': "50",
                    'frmPrincipal:Tabela_skipChildren': "true",
                    'frmPrincipal:Tabela_encodeFeature': "true",
                    'frmPrincipal': "frmPrincipal",
                    'frmPrincipal:j_idt135': "orgao",
                    'frmPrincipal:ano_focus': "",
                    'frmPrincipal:ano_input': "2022",
                    'frmPrincipal:mes_focus': "",
                    'frmPrincipal:mes_input': "06",
                    'frmPrincipal:selOrgao_focus': "",
                    'frmPrincipal:selOrgao_input': "4",
                    'javax.faces.ViewState': self.VIEWSTATE
                }
            )
        else:
            data.update(
                {
                    'javax.faces.partial.ajax': 'true',
                    'javax.faces.source': 'frmPrincipal:botaoPesquisar',
                    'javax.faces.partial.execute': '@all',
                    'javax.faces.partial.render': 'frmPrincipal:Tabela',
                    'frmPrincipal:botaoPesquisar': 'frmPrincipal:botaoPesquisar',
                    'frmPrincipal': "frmPrincipal",
                    'frmPrincipal:j_idt135': "orgao",
                    'frmPrincipal:ano_focus': "",
                    'frmPrincipal:ano_input': "2022",
                    'frmPrincipal:mes_focus': "",
                    'frmPrincipal:mes_input': "06",
                    'frmPrincipal:selOrgao_focus': "",
                    'frmPrincipal:selOrgao_input': self.orgao,
                    'javax.faces.ViewState': self.VIEWSTATE
                }
            )

        self.servidores_ja_vistos = self.servidores_ja_vistos + 50
        r = requests.post(self.URL, data=data, headers=self.HEADERS, cookies=cookies)
        self.PAGE = r.text
        self.status_code = r.status_code

    def has_next(self) -> bool:
        return self.servidores_ja_vistos < self.total_servidores
