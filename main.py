import json
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

from src.constants.paths import *
from src.constants.portal_sp import *
from src.constants.html_tags import *

from src.parser.PortalSCParser import PortalSCParser
from src.parser.PortalSPParser import PortalSPParser

from src.util import print_when_debug_enabled

URL_PORTAL_SC = "http://www.transparencia.sc.gov.br/remuneracao-servidores"

if __name__ == '__main__':
    load_dotenv('/home/duda/INE5454/.env')

    scParser = PortalSCParser(os.path.join(RESOURCES_DIR, SC_RESOURCES_DIR))

    driver = webdriver.Firefox()
    driver.get(URL_PORTAL_SC)
    driver.maximize_window()
    time.sleep(10)
    selectWebElement = driver.find_element(
        By.CSS_SELECTOR, "select[ng-model='filtros.situacao']")
    select = Select(selectWebElement)
    select.select_by_visible_text('Ativo')
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    servidores = scParser.parse(soup)
    print(servidores[0])
    num_ultima_pagina = int(driver.find_element(
        By.CSS_SELECTOR, "a[ng-click='lastPage()']").text)
    print(f'Quantidade de páginas = {num_ultima_pagina}')
    for page_number in range(2, num_ultima_pagina):
        time.sleep(10)
        botao_proximo = driver.find_element(
            By.CSS_SELECTOR, "a[ng-click='nextPage()']").click()
        time.sleep(10)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        servidores_pagina = scParser.parse(soup)
        servidores.extend(servidores_pagina)
        print(
            f'Página: {page_number}. Qtd de servidores encontrados: {servidores_pagina.__len__()}')
        print(servidores_pagina[0])
    # print(servidores)

    # driver.quit()

    # spParser = PortalSPParser(os.path.join(RESOURCES_DIR, SP_RESOURCES_DIR))

    # servidoresSC = scParser.parse_resources()
    # servidoresSP = spParser.parse_resources()

    # servidores = servidoresSC + servidoresSP

    # print_when_debug_enabled(
    #     f'Quantidade de servidores encontrados: {servidores.__len__()}')

    # result_path = os.path.join(
    #     RESOURCES_DIR, RESULT_FOLDER, RESULT_FILENAME)
    # os.makedirs(os.path.dirname(result_path), exist_ok=True)
    # with open(result_path, 'w', encoding='utf-8') as outfile:
    #     json.dump(servidores, outfile, indent=4, ensure_ascii=False)
    #     print(
    #         f'[SUCESSO] Os dados processados se encontram no arquivo {result_path}')
