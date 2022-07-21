from functools import reduce
from typing import Dict, List
import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from src.constants.angular import NG_MODEL

from src.constants.common import DEFAULT_TIME_TO_WAIT
from src.constants.portal_sc import TODOS_OS_ORGAOS
from src.parser.PortalSCParser import PortalSCParser
from src.model.EnvironmentEnum import EnvironmentEnum
from src.util import print_success_message, print_when_debug_enabled, print_error_message, print_info_message, convert_BR_number_to_EN_number
from src.crawler.PortalSCCrawlerState import PortalSCCrawlerState


class PortalSCCrawler():
    def __init__(self, portal_url: str, max_pages_to_parse: int = 20):
        self.max_pages_to_parse = max_pages_to_parse
        self.portal_url = portal_url
        self.parser = PortalSCParser()
        self.driver = webdriver.Firefox()
        self.servidores_extraidos: List[Dict] = []
        self.time_to_wait = int(os.environ.get(
            EnvironmentEnum.SELENIUM_TIME_TO_WAIT, DEFAULT_TIME_TO_WAIT))
        self.state = PortalSCCrawlerState()

    def open(self):
        self.driver.get(self.portal_url)

    def crawl(self, options: list[str] = [TODOS_OS_ORGAOS]) -> list[dict]:
        self.open()

        time.sleep(self.time_to_wait)
        selectWebElement = self.driver.find_element(
            By.CSS_SELECTOR, f"select[{NG_MODEL}='filtros.orgao']")
        select = Select(selectWebElement)

        try:
            for option in options:
                if option == TODOS_OS_ORGAOS:
                    continue

                time.sleep(self.time_to_wait)
                select.select_by_visible_text(option)
                time.sleep(self.time_to_wait)

                print_when_debug_enabled(
                    f'======= Situação: {option}')

                self.extract_data_to_validate()

                self.state.actual_processing_situacao = option
                self.extract_by_situacao()
                self.state.full_extracted_situacoes.append(option)

                if not self.isValid():
                    break
        except Exception as e:
            print_error_message('Um erro aconteceu. Estado do Crawler:')
            print(self.state.__str__())
            print(f'Mensagem do erro: {e.__str__()}')
        finally:
            self.driver.quit()
            return self.servidores_extraidos

    def extract_by_situacao(self):
        try:
            num_ultima_pagina = int(self.driver.find_element(
                By.CSS_SELECTOR, "a[ng-click='lastPage()']").text)
        except (NoSuchElementException, ValueError):
            return None

        self.state.total_of_pages_processing_situacao = num_ultima_pagina
        print_when_debug_enabled(
            f'Quantidade de páginas = {num_ultima_pagina}')

        print_info_message('Extraindo os dados...')
        self.extract_first_page()
        self.iterate_over_pages(num_ultima_pagina)

    def extract_first_page(self):
        self.state.actual_processing_situacao_page = 1
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        servidores = self.parser.parse(soup)
        self.servidores_extraidos.extend(servidores)
        self.state.print_actual_state()

    def iterate_over_pages(self, num_ultima_pagina: int) -> list[dict]:
        pages_parsed = 1
        for page_number in range(2, num_ultima_pagina + 1):
            if pages_parsed > self.max_pages_to_parse:
                break
            self.state.actual_processing_situacao_page = page_number

            time.sleep(self.time_to_wait)
            botao_proximo = self.driver.find_element(
                By.CSS_SELECTOR, '[ng-click="nextPage()"]')
            botao_proximo.click()
            time.sleep(self.time_to_wait)

            print_when_debug_enabled(
                f'Página: {page_number}. Extraindo dados...')

            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            servidores_pagina = self.parser.parse(soup)
            self.servidores_extraidos.extend(servidores_pagina)

            print_when_debug_enabled(
                f'Página: {page_number}. Quantidade servidores encontrados: {servidores_pagina.__len__()}')
            self.state.print_actual_state()
            pages_parsed = pages_parsed + 1

    def extract_data_to_validate(self):
        print_info_message('Extraindo dados para validação...')

        total_valor_bruto = self.driver.find_element(
            By.CSS_SELECTOR, "div[class='conteudo-bloco-filtro-resultados-valor'] > div").text
        total_servidores = self.driver.find_element(
            By.CSS_SELECTOR, "div[class='conteudo-bloco-filtro-resultados-valor valor-pessoas'] > div").text

        self.total_valor_bruto = float(convert_BR_number_to_EN_number(
            total_valor_bruto))
        self.total_servidores = int(convert_BR_number_to_EN_number(
            total_servidores))

        print_when_debug_enabled(
            f'Valor bruto total = {self.total_valor_bruto}, # Servidores = {self.total_servidores}')

    def isValid(self) -> bool:
        print_info_message("Validando os dados extraídos...")

        quantidade_servidores_extraidos = self.servidores_extraidos.__len__()
        if self.total_servidores == quantidade_servidores_extraidos:
            print_success_message(
                f"Quantida de servidores: OK [{self.total_servidores}]")

            total_bruto = reduce(
                lambda a, b: a + b, self.servidores_extraidos, 0.0)
            if self.total_valor_bruto == total_bruto:
                print_success_message(
                    f"Valor bruto total: OK [{self.total_valor_bruto}]")
                return True
            else:
                print_error_message(
                    f"O valor bruto total dos dados extraídos foi {total_bruto} sendo que deveria ser {self.total_valor_bruto}")
        else:
            print_error_message(
                f"A quantidade de servidores extraídos foi {quantidade_servidores_extraidos} sendo que deveria ser {self.total_servidores}")
        return False
