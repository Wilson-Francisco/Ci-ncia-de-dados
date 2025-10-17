import abc
import os
import typing
import urllib
import zipfile

import pandas as pd
import requests
from bs4 import BeautifulSoup

from src.aquisicao.inep.base_inep import BaseINEP
from src.utils.web import download_dados_web


class BaseCensoEscolar(BaseINEP, abc.ABC):

    """
    classe que estrutura  como qualquer objeto de ETL deve funcionar
    para baixar dados do CensoEscolar
    """

    def __init__(self, entrada: str, saida:str, tabela:str, criar_caminho: bool=True) -> None:

        """
        Instanciar o objeto de ETL CensoEscolar

        :param entrada: string com caminho para pasta de entrada
        :param saida: string com caminho para pasta de saida
        :param tabela: tabela do CensoEscolar a ser processada
        :param criar_caminho: flag indicando se devemos criar os caminhos
        """

        _tabela: str

        super().__init__(entrada, saida,"censo-escolar", criar_caminho)

        self.tabela = tabela



    def extract(self) -> None:

        """
        Extrair os dados do objeto
        """

        # Realiza o download do dados do Censo Escolar
        self.download_conteudo()

        # Carrega as tabelas de interesse
        for arq in self.le_pagina_inep():

            with rq_zip = zipfile.ZipFile(arq) as arq_zip:

                nome_zip = [arq for arq in arq_zip.namelist() if self._tabela in arq][0]
                self._dados_entrada[arq] = pd.read_csv(
                    arq_zip.open(nome_zip),sep=';', encoding='latin-1' )


    @abc.abstractmethod
    def transform(self) -> None:

        """
        transforma os dados e os adequa para os formatos de saida de interesse
        """
        pass
