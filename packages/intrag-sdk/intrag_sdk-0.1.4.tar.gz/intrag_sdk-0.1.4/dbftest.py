from dbfread import DBF


b = open("POSICOTI.dbf", "rb").read()

file = DBF("POSICOTI.dbf", encoding="latin1")

df = file.to_dataframe()

print(df)
