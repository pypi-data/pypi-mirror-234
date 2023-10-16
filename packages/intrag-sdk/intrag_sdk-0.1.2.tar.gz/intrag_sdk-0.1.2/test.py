from intrag_sdk import ItauPassivo, TipoArquivo, Arquivo
import pandas as pd

user = "rps.op04"
password = "996329"

api = ItauPassivo(echo=True)
api.authenticate(user=user, password=password)

# Propriedades disponíveis
nome_gestor: str = api.nome_gestor
codigo_gestor: str = api.codigo_gestor
fundos: pd.DataFrame = api.fundos

# Consultas
# movimentacoes: pd.DataFrame = api.movimentos_do_dia()

codigo_fundo: str = fundos["codigoFundo"][0]

# posicoes: pd.DataFrame = api.posicao_cotistas(codigo_fundo=codigo_fundo)
