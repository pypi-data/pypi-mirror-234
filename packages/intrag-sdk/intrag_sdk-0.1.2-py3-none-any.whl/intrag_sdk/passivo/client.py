import requests
import bs4
import re
import datetime
import pandas as pd
import xml.etree.ElementTree as ET
from intrag_sdk.passivo.file_types import TipoArquivo, Arquivo
import zipfile
import io

DEFAULT_ENCODING = "ISO-8859-1"


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
        def fetch_code_and_name():
            res = self.post(
                "/listarFundosConsultaMovimentoFundoTotaisXML.do",
                data={"codigoGestor": self.codigo_gestor},
            )

            root = ET.fromstring(res.text)
            fundos = []
            for fundo in root.iter("FundoForm"):
                codigo_fundo = fundo.find("codigoFundo")
                nome_fundo = fundo.find("nomeFundo")

                if codigo_fundo is None or nome_fundo is None:
                    continue

                fundos.append(
                    {"codigoFundo": codigo_fundo.text, "nomeFundo": nome_fundo.text}
                )

            return pd.DataFrame(fundos)[["codigoFundo", "nomeFundo"]]

        def fetch_cnpj():
            archive = self.download_de_arquivos(
                TipoArquivo.TXT, Arquivo.CADASTRO_DE_FUNDOS
            )

            text = archive.read(archive.filelist[0]).decode("utf-8")

            def get_cnpj(row):
                pattern = r"[A-Za-z\s]0\d{14}"
                result = re.search(pattern, row)
                if not result:
                    return None

                return result.group(0)[2:16]

            def get_fund_code(row):
                pattern = r"\d{5}[A-Za-z\s]"
                result = re.search(pattern, row)
                if not result:
                    return row

                return result.group(0)[:-1]

            def get_fund_info(row):
                cnpj = get_cnpj(row)
                fund_code = get_fund_code(row)
                return {"codigoFundo": fund_code, "cnpj": cnpj}

            data = list(map(get_fund_info, text.strip().split("\n")))
            return pd.DataFrame(data)

        codes = fetch_code_and_name()
        cnpjs = fetch_cnpj()

        self.fundos = codes.merge(cnpjs, on="codigoFundo")

    def download_de_arquivos(
        self,
        tipo_arquivo: TipoArquivo,
        arquivo: Arquivo,
        data: datetime.date = datetime.date.today(),
    ):
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

        return zipfile.ZipFile(io.BytesIO(res.content), "r")

    def posicao_cotistas(self, codigo_fundo: str):
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
