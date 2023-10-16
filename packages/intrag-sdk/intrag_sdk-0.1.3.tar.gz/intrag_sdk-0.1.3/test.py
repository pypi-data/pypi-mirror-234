import datetime
from typing import List
from zipfile import ZipFile
from intrag_sdk import ItauPassivo, TipoArquivo, Arquivo
import pandas as pd
from intrag_sdk.passivo.client import Download
from intrag_sdk.simpledbf import Dbf5

user = "rps.op04"
password = "996329"

api = ItauPassivo(echo=True)
api.authenticate(user=user, password=password)

# Propriedades disponíveis
nome_gestor: str = api.nome_gestor
codigo_gestor: str = api.codigo_gestor
fundos: pd.DataFrame = api.fundos


# Download de arquivos
downloads: List[Download] | ZipFile = api.download_de_arquivos(
    Arquivo.ARQUIVO_DE_PERFORMANCE, data=datetime.date(2023, 10, 6)
)

# Movimentações do dia
movimentacoes: pd.DataFrame = api.movimentos_do_dia()

# Posição de cotistas
codigo_fundo: str = fundos["CDFDO"][0]

posicoes: pd.DataFrame = api.posicao_cotistas(codigo_fundo=codigo_fundo)
