from bs4 import BeautifulSoup

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
    with open('resources/sp/prof_1/Remuneracao.html', 'r') as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        result = soup.find('table', attrs={'rules': 'all'})
        trs = result.find_all('tr', attrs=None)
        infos_salariais = dict()
        n_entradas = 0;
        for tr in trs:
            tds = tr.find_all('td')
            if len(tds) < 1:
                continue
            line = dict()
            for i in range(10):
                line.update({NOME_CAMPOS[i]: tds[i].text})
            infos_salariais.update({n_entradas: line})
            n_entradas = n_entradas + 1
        print('bk')
