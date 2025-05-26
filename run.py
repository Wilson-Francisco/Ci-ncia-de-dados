import click
from src.aquisicao.opcoes import EnumETL
from src.aquisicao.opcoes import ETL_DICT
import src.configs as conf_geral



@click.group()
def cli():
  pass


@cli.group()
def aquisicao():

    """
      Grupo decomandos que executam as funcoes de aquisicao
    """


@aquisicao.command()
@click.option("--etl", type=click.Choice([s.value for s in EnumETL]), help='Nome do ETL a ser executado.')
@click.option('--entrada', default=conf_geral.PASTA_DADOS, help='String com caminho para pasta de entrada.')
@click.option('--saida', default=conf_geral.PASTA_SAIDA_AQUISICAO, help='String com caminho para pasta de saida.')
@click.option('--criar_caminho', default=True, help='Flag indicando se devemos criar os caminho.')
def processa_dado(etl: str, entrada: str, saida: str, criar_caminho: bool) -> None:

    """
    Executa o pipeline de ETL de uma determinada fonte
    :param etl: nome do ETL a ser executado
    :param entrada: string com caminho para pasta de entrada
    :param saida: string com caminho para pasta de saida
    :param criar_caminho: flag indicando se devemos criar os caminhos
    """


    objeto = ETL_DICT[EnumETL(etl)](entrada, saida, criar_caminho)

    objeto.pipeline()






if __name__ == '__main__':

    cli()