import requests
import bs4
import re
import datetime
import pandas as pd
import xml.etree.ElementTree as ET

DEFAULT_ENCODING = "ISO-8859-1"


class ItauPassivo:
    headers = {
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
    }

    def __init__(self):
        self.base_url = "https://www.itaucustodia.com.br/Passivo"
        self.cookies = {}

    def endpoint(self, path: str):
        return f"{self.base_url}{path}"

    def post(self, endpoint: str, data: dict = dict()):
        form_data = "&".join([f"{key}={value}" for key, value in data.items()])

        res = requests.post(
            self.endpoint(endpoint),
            headers=self.headers,
            cookies=self.cookies,
            data=form_data,
        )

        return res

    def fetch_info(self):
        """Seta codigo do gestor e lista de fundos disponiveis"""
        res = self.post("/abreFiltroConsultaMovimentoFundoTotais.do")

        html = bs4.BeautifulSoup(
            res.content, "html.parser", from_encoding=DEFAULT_ENCODING
        )

        gestor = html.find("select", dict(name="codigoGestor")).find_all("option")[-1]

        codigo_gestor = gestor.attrs.get("value")
        nome_gestor = gestor.text

        res = self.post(
            "/listarFundosConsultaMovimentoFundoTotaisXML.do",
            data={"codigoGestor": codigo_gestor},
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

        fundos = pd.DataFrame(fundos)[["codigoFundo", "nomeFundo"]]

        self.nome_gestor = nome_gestor
        self.codigo_gestor = codigo_gestor
        self.fundos = fundos

    def authenticate(self, user: str, password: str):
        res = self.post("/login.do", data={"ebusiness": user, "senha": password})

        if "logoff" not in res.content.decode(encoding=DEFAULT_ENCODING):
            raise Exception("Login Inválido")

        self.cookies = {"JSESSIONID": res.cookies.get("JSESSIONID")}
        self.fetch_info()

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
