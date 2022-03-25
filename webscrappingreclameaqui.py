import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.chrome.options import Options


class Scraping:
    def __init__(self):
        self.dados_do_arquivo = {}
        self.lista_de_titulos = []
        self.lista_de_empresas = []
        self.lista_de_empresas_temporario = []
        self.lista_de_notas = []
        self.lista_de_notas_temporario = []

    def iniciar(self):
        self.acessar_paginas()
        self.rapasgem_de_dados()
        self.criar_data_frame()
        self.criar_arquivo()

    def acessar_paginas(self):
        self.navegador = webdriver.Chrome()
        self.navegador.get('https://www.reclameaqui.com.br/')
        sleep(1)

        self.pagina_ranking = self.navegador.find_elements_by_css_selector(
            'li[class="link-header"]')[2]
        self.pagina_ranking.click()
        sleep(1)

    def rapasgem_de_dados(self):
        self.site = BeautifulSoup(self.navegador.page_source, 'html.parser')

        self.tabelas_de_rankings = self.site.findAll(
            'div', attrs={'class': 'box-gray'})

        for self.tabela in self.tabelas_de_rankings:

            self.titulo_do_ranking = self.tabela.find(
                'h2', attrs={'class': 'ng-binding'})

            self.titulo_do_ranking = self.titulo_do_ranking.text
            self.lista_de_titulos.append(self.titulo_do_ranking)

            self.ranking = self.tabela.findAll(
                'div', attrs={'ng-switch': 'key'})

            for self.empresa_e_nota in self.ranking:

                self.nome_empresa = self.empresa_e_nota.find(
                    'a', attrs={'class': 'business-name ng-binding ng-scope'})
                self.nome_empresa = self.nome_empresa['title']

                self.nota = self.empresa_e_nota.find(
                    'span', attrs={'class': 'ng-binding'})
                self.nota = self.nota.text

                self.lista_de_empresas_temporario.append(self.nome_empresa)
                self.lista_de_notas_temporario.append(self.nota)

            self.lista_de_empresas.append(
                self.lista_de_empresas_temporario[:])

            self.lista_de_notas.append(
                self.lista_de_notas_temporario[:])

            self.lista_de_empresas_temporario.clear()
            self.lista_de_notas_temporario.clear()

    def criar_data_frame(self):
        for self.titulo, self.empresas, self.notas in zip(self.lista_de_titulos, self.lista_de_empresas, self.lista_de_notas):
            self.dados_do_arquivo[self.titulo] = self.empresas
            self.dados_do_arquivo[
                f'Notas da tabela n°{self.lista_de_titulos.index(self.titulo) + 1}'] = self.notas

    def criar_arquivo(self):
        self.dados = pd.DataFrame(data=self.dados_do_arquivo)
        print(self.dados)
        self.dados.to_excel('Rankings_Reclame_Aqui.xlsx', index=False)


reclame_aqui = Scraping()
reclame_aqui.iniciar()
