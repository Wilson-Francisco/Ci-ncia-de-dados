import requests
import typing
from pathlib import Path as path

import requests
from bs4 import BeautifulSoup


def download_dados_web(caminho:typing.Union[str, path], url: str ) -> None:

    """
    Realiza o download dos dados de um link da web

    :param caminho: caminho para extracao dos dados
    :param url: recebe endereco do site a ser baixado

    """

    r = requests.get(url, stream=True)
    with open(caminho, "wb") as arq:
        arq.write(r.content)