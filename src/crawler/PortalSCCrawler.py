from typing import Dict, List
from json import dump
import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from src.constants.angular import NG_MODEL

from src.constants.common import DEFAULT_TIME_TO_WAIT
from src.parser.PortalSCParser import PortalSCParser
from src.model.EnvironmentEnum import EnvironmentEnum
from src.constants.paths import *
from src.util import print_success_message, print_when_debug_enabled


class PortalSCCrawler():
    def __init__(self, portal_url: str):
        self.portal_url = portal_url
        self.parser = PortalSCParser()
        self.driver = webdriver.Firefox()
        self.result: List[Dict] = []
        self.time_to_wait = int(os.environ.get(
            EnvironmentEnum.SELENIUM_TIME_TO_WAIT, DEFAULT_TIME_TO_WAIT))

    def open(self):
        self.driver.get(self.portal_url)
        self.driver.maximize_window()

    def crawl(self) -> List[Dict]:
        self.open()

        time.sleep(self.time_to_wait)
        selectWebElement = self.driver.find_element(
            By.CSS_SELECTOR, f"select[{NG_MODEL}='filtros.situacao']")
        select = Select(selectWebElement)

        for option in select.options:
            if isinstance(option, WebElement):
                option_text = option.text
                if option_text == 'Todas as situações':
                    continue
                time.sleep(self.time_to_wait)
                select.select_by_visible_text(option_text)
                time.sleep(self.time_to_wait)
                print_when_debug_enabled(f'======= Situação: {option_text}')
                self.extract_by_situacao()

        self.driver.quit()
        self.export_to_json()

    def extract_by_situacao(self):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        servidores = self.parser.parse(soup)
        self.result.extend(servidores)

        num_ultima_pagina = 1
        try:
            num_ultima_pagina = int(self.driver.find_element(
                By.CSS_SELECTOR, "a[ng-click='lastPage()']").text)
        except (NoSuchElementException, ValueError):
            return servidores

        print_when_debug_enabled(
            f'Quantidade de páginas = {num_ultima_pagina}')
        self.iterate_over_pages(num_ultima_pagina)

    def iterate_over_pages(self, num_ultima_pagina: int) -> List[Dict]:
        servidores_paginas = []

        for page_number in range(2, num_ultima_pagina + 1):
            print_when_debug_enabled(
                f'Página: {page_number}. Extraindo dados...')

            time.sleep(self.time_to_wait)
            botao_proximo = self.driver.find_element(
                By.CSS_SELECTOR, "a[ng-click='nextPage()']")
            botao_proximo.click()
            time.sleep(self.time_to_wait)

            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            servidores_pagina = self.parser.parse(soup)
            servidores_paginas.extend(servidores_pagina)
            print_when_debug_enabled(
                f'Página: {page_number}. Quantidade servidores encontrados: {servidores_pagina.__len__()}')

        self.result.extend(servidores_paginas)

    def export_to_json(self):
        print_when_debug_enabled(
            f'Exportando {self.result.__len__()} servidores...')
        result_path = os.path.join(RESULT_FOLDER, 'SC/', RESULT_FILENAME)
        os.makedirs(os.path.dirname(result_path), exist_ok=True)
        with open(result_path, 'w', encoding='utf-8') as outfile:
            dump(self.result, outfile, indent=4, ensure_ascii=False)
            print_success_message(
                f'Os dados processados se encontram no arquivo {result_path}')
