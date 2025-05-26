import abc
from operator import index
from pathlib import Path as path
import typing
import pandas as pd

class BaseETL(abc.ABC):

    """
    classe que estrutura  como qualquer objeto de ETL deve funcionar
    """

    caminho_entrada: path
    caminho_saida: path
    _dados_entrada: typing.Dict[str, pd.DataFrame]
    _dados_saida: typing.Dict[str, pd.DataFrame]


    def __init__(self, entrada: str, saida:str, criar_caminho: bool=True) -> None:


        """
        Instanciar o objeto de ETL Base
        :param entrada: string com caminho para pasta de entrada
        :param saida: string com caminho para pasta de saida
        :param criar_caminho: flag indicando se devemos criar os caminhos
        """

        self.caminho_entrada = path(entrada)
        self.caminho_saida = path(entrada)


        if criar_caminho:
            self.caminho_entrada.mkdir(parents=True, exist_ok=True)
            self.caminho_saida.mkdir(parents=True, exist_ok=True)


        self._dados_entrada = None
        self._dados_saida = None


    @property
    def dados_entrada(self) -> typing.Dict[str, pd.DataFrame]:


        """
        Acessa o dicionario de dados de entrada
        :return: dicionario comnome do arquivo e dataframe com os dados
        """


        if self._dados_entrada is None:
            self.transform()

        return self._dados_entrada




    @property
    def dados_saida(self) -> typing.Dict[str, pd.DataFrame]:

        """
        Acessa o dicionario de dados de saida
        :return: dicionario comnome do arquivo e dataframe com os dados
        """

        if self._dados_saida is None:
            self.transform()

        return self._dados_saida



    @abc.abstractmethod
    def extract(self) -> None:

        """
        Extrair os dados do objeto
        """


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

        for arq, df in self._dados_saida.items():
            df.to_parquet(self.caminho_saida / arq, index=False)



    def pipeline(self) -> None:

        """
        Executa o pipeline completo de tratamento de dados
        """

        self.extract()
        self.transform()
        self.load()