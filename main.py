import json
import os

from bs4 import BeautifulSoup


BASE_SP_FILE_DIR = 'resources/sp/'
JOB_1 = 'secretaria_dos_esportes/'
FILE_EXTENSION = '.html'
RESULT_FOLDER = 'result/'

NOME = 'NOME'
ORGAO = 'ORGAO'
CARGO = 'CARGO'
REMUNERACAO_MES = 'REMUNERACAO_DO_MES'
FERIAS_E_13_SALARIO = 'FERIAS_E_13_SALARIO'
PAGAMENTOS_EVENTUAIS = 'PAGAMENTOS_EVENTUAIS'
LICENCA_PREMIO_INDENIZADA = 'LICENCA_PREMIO_INDENIZADA'
ABONO_PERMANENCIA_E_OUTRAS_INDENIZACOES = 'ABONO_PERMANENCIA_E_OUTRAS_INDENIZACOES'
REDUTOR_SALARIAL = 'REDUTOR_SALARIAL'
TOTAL_LIQUIDO = 'TOTAL_LIQUIDO'
NOME_CAMPOS = [NOME, ORGAO, CARGO, REMUNERACAO_MES, FERIAS_E_13_SALARIO, PAGAMENTOS_EVENTUAIS, LICENCA_PREMIO_INDENIZADA, ABONO_PERMANENCIA_E_OUTRAS_INDENIZACOES, REDUTOR_SALARIAL, TOTAL_LIQUIDO]

# https://stackabuse.com/guide-to-parsing-html-with-beautifulsoup-in-python/ <<<<<====== link de guia para uso da ferramenta

if __name__ == '__main__':
    infos_salariais = dict()
    n_entradas = 1;

    # itera pelas paginas salvas em um diretorio qualquer
    for page in range (1, len(os.listdir(BASE_SP_FILE_DIR+JOB_1))):
       # abre uma pagina qualquer
       with open(BASE_SP_FILE_DIR + JOB_1 + str(page) + FILE_EXTENSION, 'r') as fp:
            soup = BeautifulSoup(fp, 'html.parser')
            # acha a tag com as informacoes desejadas
            result = soup.find('table', attrs={'rules': 'all'})
            # obtem o elemento de linha de tabela contida na tabela desejada
            trs = result.find_all('tr', attrs=None)
            # itera sobre os elementos linha
            for tr in trs:
                tds = tr.find_all('td')
                # checa se uma linha contem apenas infos de cabecalho; se sim vai para proxima
                if len(tds) < 1:
                    continue
                line = dict()
                # cria um dicionario com as informacoes de uma linha
                for i in range(10):
                    line.update({NOME_CAMPOS[i]: tds[i].text})
                # atualiza o dicionario principal
                infos_salariais.update({n_entradas: line})
                n_entradas = n_entradas + 1

            # apenas imprime o dicionario obtido
            for i, info in infos_salariais.items():
                print(i, '->', info)

    # escreve os dados serializados para um arquivo qualquer
    filename = BASE_SP_FILE_DIR + JOB_1 + RESULT_FOLDER + 'data.json'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as outfile:
        json.dump(infos_salariais, outfile)
