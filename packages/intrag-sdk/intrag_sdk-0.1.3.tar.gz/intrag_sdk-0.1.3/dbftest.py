from simpledbf import Dbf5


file = Dbf5("CADFUN.dbf")

df = file.to_dataframe()

print(df)
