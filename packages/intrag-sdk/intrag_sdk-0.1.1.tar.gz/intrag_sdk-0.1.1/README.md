# intrag-sdk

SDK não oficial do Itau Investiment Services

## Passivo

Exemplo de uso do **crawler** para consultas no site https://www.itaucustodia.com.br/Passivo

```python
from intrag_sdk import ItauPassivo
import pandas as pd

api = ItauPassivo()
api.authenticate(user="usuario123", password="123456")

# Propriedades disponíveis
nome_gestor: str = api.nome_gestor
codigo_gestor: str = api.codigo_gestor
fundos: pd.DataFrame = api.fundos

# Movimentações do dia
movimentacoes: pd.DataFrame = api.movimentos_do_dia()

# Posição de cotistas
codigo_fundo: str = fundos["codigoFundo"][0]

posicoes: pd.DataFrame = api.posicao_cotistas(codigo_fundo=codigo_fundo)
```
