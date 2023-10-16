from intrag_sdk import ItauPassivo
import pandas as pd

user = "usuário"
password = "senha"

api = ItauPassivo()
api.authenticate(user=user, password=password)

# Propriedades disponíveis
nome_gestor: str = api.nome_gestor
codigo_gestor: str = api.codigo_gestor
fundos: pd.DataFrame = api.fundos

# Consultas
movimentacoes: pd.DataFrame = api.movimentos_do_dia()

codigo_fundo: str = fundos["codigoFundo"][0]

posicoes: pd.DataFrame = api.posicao_cotistas(codigo_fundo=codigo_fundo)
