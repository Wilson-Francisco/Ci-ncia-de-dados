import abc
import os
import typing
import urllib

import requests
from bs4 import BeautifulSoup

from src.aquisicao.base_etl import BaseETL
from src.utils.web import download_dados_web


class BaseINEP(BaseETL, abc.ABC):

    """
    classe que estrutura  como qualquer objeto de ETL deve funcionar
    para baixar dados do INEP
    """

    URL: str = "https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados"


    def __init__(self, entrada: str, saida:str, base:str, criar_caminho: bool=True) -> None:

        """
        Instanciar o objeto de ETL INEP
        :param entrada: string com caminho para pasta de entrada
        :param saida: string com caminho para pasta de saida
        :param base: Nome da base que vai na URL do INEP
        :param criar_caminho: flag indicando se devemos criar os caminhos
        """

        super().__init__(entrada, saida, criar_caminho)

        self._url = f"{self.URL}/{base}"

    def le_pagina_inep(self) -> typing.Dict[str, str]:

        """
        Realiza o web-scraping da pagina de dados do INEP
        :return: ndicionario com nome do arquivo e link para pagina
        """

        html = urllib.request.urlopen(self._url).read()

        soup = BeautifulSoup(html, features="lxml")

        return {tag["href"].split("_")[-1]: tag["href"] for tag in soup.find_all("a", {"class": "external-link"})}



    def dicionario_para_baixar(self) ->typing.Dict[str, str]:

        """
        Le os conteudos da pasta de dados e seleciona apenas os arquivos
        a serem baixados como complementares
        :return: dicionario com nome do arquivo e link para pagina
        """

        para_baixar = self.le_pagina_inep()

        baixados = os.listdir(str(self.caminho_entrada))

        return { arq: link for arq, link in para_baixar.items() if arq not in baixados }


    def download_conteudo(self) ->None:

        """
        Realizadoo download dos dados INEP para uma pasta local
        """

        for arq, link in self.dicionario_para_baixar():
            caminho_arq = self.caminho_saida/arq
            download_dados_web(caminho_arq,link)


    @abc.abstractmethod
    def extract(self) -> None:

        """
        Extrair os dados do objeto
        """
        pass

    @abc.abstractmethod
    def transform(self) -> None:

        """
        transforma os dados e os adequa para os formatos de saida de interesse
        """
        pass


    @abc.abstractmethod
    def load(self) -> None:

        """
        Exporta os dados transformados

        """

        for arq, df in self.dados_saida.items():
            df.to_parquet(self.caminho_saida / arq, index=False)



    def pipeline(self) -> None:

        """
        Executa o pipeline completo de tratamento de dados
        """

        self.extract()
        self.transform()
        self.load()