import pandas as pd

df_confesiuni = pd.read_csv("data_in/Religious.csv", index_col=0)

# print(df_confesiuni, type(df_confesiuni))

confesiuni = list(df_confesiuni)[1:]
df_coduri_loc = pd.read_csv("data_in/Coduri_Localitati.csv")
df_confesiuni_loc = df_confesiuni[confesiuni].merge(df_coduri_loc, left_index=True)

df_confesiuni_jud = df_confesiuni_loc[confesiuni + ["County"]].groupby(by=["Country"])
df_confesiuni_jud.to_csv("data_out/Confesiuni_jud.csv")

