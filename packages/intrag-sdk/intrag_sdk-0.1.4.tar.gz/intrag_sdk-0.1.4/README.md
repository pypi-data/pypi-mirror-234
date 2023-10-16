<h1 align="center">
intrag-sdk
</h1>

<p align="center">
    <em>SDK não oficial do Itau Investiment Services</em>
</p>

## Instalação

```bash
$ pip install intrag_sdk
```

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


# Download de arquivos
downloads: List[Download] | ZipFile = api.download_de_arquivos(
    Arquivo.ARQUIVO_DE_PERFORMANCE, data=datetime.date(2023, 10, 6)
)

# Movimentações do dia
movimentacoes: pd.DataFrame = api.movimentos_do_dia()

# Posição de cotistas
codigo_fundo: str = fundos["CDFDO"][0]

posicoes: pd.DataFrame = api.posicao_cotistas(codigo_fundo=codigo_fundo)
```
