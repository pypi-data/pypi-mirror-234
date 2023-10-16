from dataclasses import dataclass
from typing import List, Union, cast
import requests
import bs4
import re
import datetime
import pandas as pd
import xml.etree.ElementTree as ET
from intrag_sdk.passivo.file_types import TipoArquivo, Arquivo
import zipfile
import io

from intrag_sdk.simpledbf import Dbf5

DEFAULT_ENCODING = "ISO-8859-1"
DEFAULT_FILE_ENCODING = "latin1"


class FileNotFound(Exception):
    pass


@dataclass
class Download:
    file_name: str
    data: Union[str, pd.DataFrame]


class ItauPassivo:
    headers = {
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
    }

    def __init__(self, echo=False):
        self.base_url = "https://www.itaucustodia.com.br/Passivo"
        self.cookies = {}
        self.echo = echo

    def endpoint(self, path: str):
        return f"{self.base_url}{path}"

    def post(self, endpoint: str, data: dict = dict()):
        if self.echo:
            print(f"POST {endpoint}")
            print(data)

        form_data = "&".join([f"{key}={value}" for key, value in data.items()])

        res = requests.post(
            self.endpoint(endpoint),
            headers=self.headers,
            cookies=self.cookies,
            data=form_data,
        )

        self.cookies = {**self.cookies, **res.cookies.get_dict()}

        return res

    def __fetch_gestor_info(self):
        """Seta codigo do gestor e lista de fundos disponiveis"""
        res = self.post("/abreFiltroConsultaMovimentoFundoTotais.do")

        html = bs4.BeautifulSoup(
            res.content, "html.parser", from_encoding=DEFAULT_ENCODING
        )

        gestor = html.find("select", dict(name="codigoGestor")).find_all("option")[-1]

        codigo_gestor = gestor.attrs.get("value")
        nome_gestor = gestor.text

        self.nome_gestor = nome_gestor
        self.codigo_gestor = codigo_gestor

    def authenticate(self, user: str, password: str):
        res = self.post("/login.do", data={"ebusiness": user, "senha": password})

        if "logoff" not in res.content.decode(encoding=DEFAULT_ENCODING):
            raise Exception("Login Inválido")

        self.cookies = {"JSESSIONID": res.cookies.get("JSESSIONID")}
        self.__fetch_gestor_info()
        self.__fetch_funds_info()

    def __fetch_funds_info(self):
        try:
            downloads = self.download_de_arquivos(arquivo=Arquivo.CADASTRO_DE_FUNDOS)

            downloads = cast(List[Download], downloads)

            self.fundos = cast(pd.DataFrame, downloads[0].data)

        except FileNotFound:
            self.fundos = pd.DataFrame()

    def download_de_arquivos(
        self,
        arquivo: Arquivo,
        tipo_arquivo: TipoArquivo = TipoArquivo.DBF,
        data: datetime.date = datetime.date.today(),
        raw: bool = False,
        encoding: str = DEFAULT_FILE_ENCODING,
    ) -> Union[List[Download], zipfile.ZipFile]:
        """
        Baixa arquivos do servidor e retorna uma lista de objetos Download ou um arquivo zip, dependendo do valor do parâmetro raw.

        Argumentos:
            tipo_arquivo (TipoArquivo): O tipo de arquivo a ser baixado.
            arquivo (Arquivo): O arquivo a ser baixado.
            data (datetime.date, opcional): A data do arquivo a ser baixado. O padrão é a data de hoje.
            raw (bool, opcional): Se True, retorna um arquivo zip. Se False, retorna uma lista de objetos Download. O padrão é False.

        Retorna:
            Union[List[Download], zipfile.ZipFile]: Uma lista de objetos Download ou um arquivo zip, dependendo do valor do parâmetro raw.
        """

        date_str = data.strftime("%d%m%Y")

        self.post(
            "/listarOpcoesArquivosDownloadArquivos.do",
            data={
                "codigoGestor": self.codigo_gestor,
                "tipoArquivo": tipo_arquivo.value,
                "data": date_str,
            },
        )

        self.post(
            "/processarDownloadArquivosAjax.do",
            data={
                "codigoGestor": self.codigo_gestor,
                "tipoArquivo": tipo_arquivo.value,
                "numeroArquivo": arquivo.value,
            },
        )

        res = self.post(
            "/EfetuarDownloadArquivosListaServlet",
            data={
                "checkArquivos": arquivo.value,
                "numerosArquivosSelecionados": arquivo.value,
            },
        )

        if "zip" not in res.headers["Content-Type"]:
            raise FileNotFound("Arquivo não encontrado")

        archive = zipfile.ZipFile(io.BytesIO(res.content), "r")

        if raw:
            return archive

        downloads = []

        for file in archive.filelist:
            raw_file_data = archive.read(file)

            file_data = None

            if tipo_arquivo == TipoArquivo.DBF:
                df = Dbf5(raw_file_data, encoding).to_dataframe()
                file_data = cast(pd.DataFrame, df)

            if tipo_arquivo == TipoArquivo.TXT:
                file_data = raw_file_data.decode(encoding)

            if file_data is not None:
                downloads.append(Download(file_name=file.filename, data=file_data))

        return downloads

    def posicao_cotistas(self, codigo_fundo: str):
        """
        codigo_fundo (str): Pode ser encontrado em 'fundos'

        ```
        client = ItauPassivo()
        client.fundos["CDFDO"].
        ```
        """

        data = {
            "codigoGestor": self.codigo_gestor,
            "codigoFundo": codigo_fundo,
        }

        res = self.post("/consultarCotistasFundo.do", data=data)

        html = make_soup(res)

        tables = html.find("div", {"id": "listaDados"}).find_all("table")

        data = list(map(parse_table, tables))

        return pd.DataFrame(data)

    def movimentos_do_dia(
        self,
    ):
        data = {
            "codigoGestor": self.codigo_gestor,
        }

        res = self.post("/consultarMovimentoDia.do", data=data)

        html = make_soup(res)

        movimentos_dia = html.find("span", string="Movimentos do Dia")

        if movimentos_dia is None:
            return pd.DataFrame()

        tables = movimentos_dia.find_next_siblings("table")[:-2]

        data = list(map(parse_table, tables))

        return pd.DataFrame(data)


def make_soup(res, encoding=DEFAULT_ENCODING):
    return bs4.BeautifulSoup(res.content, "html.parser", from_encoding=encoding)


def parse_table(table):
    tds = table.find_all("td")

    td_tuples = [(tds[i], tds[i + 1]) for i in range(0, len(tds), 2)]

    def parse_key(td):
        return td.text.strip()[:-1]

    def parse_value(td):
        text = td.text.strip()

        _text = text.replace(".", "").replace(",", "")

        if _text.isnumeric():
            return float(text.replace(".", "").replace(",", "."))

        regex = r"(\d{2})/(\d{2})/(\d{4})"

        if re.match(regex, text):
            return datetime.datetime.strptime(text, "%d/%m/%Y").date()

        return text

    return {parse_key(key): parse_value(value) for key, value in td_tuples}
