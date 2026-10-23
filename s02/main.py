import pandas as pd

from functii import shannon, simpson, inverse_simpson
from s02.functii import diversitate

df_confesiuni = pd.read_csv("data_in/Religious.csv", index_col=0)

# print(df_confesiuni, type(df_confesiuni))

confesiuni = list(df_confesiuni)[1:]
df_coduri_loc = pd.read_csv("data_in/Coduri_Localitati.csv", index_col=0)
df_confesiuni_loc = df_confesiuni[confesiuni].merge(df_coduri_loc, left_index=True, right_index=True)

df_confesiuni_jud = df_confesiuni_loc[confesiuni + ["County"]].groupby(by=["County"]).sum()
df_confesiuni_jud.to_csv("data_out/Confesiuni_jud.csv")

df_coduri_jud = pd.read_csv("data_in/Coduri_Judete.csv", index_col=0)
df_confesiuni_jud_reg = df_confesiuni_jud.merge(df_coduri_jud, left_index=True, right_on="IndicativJudet")
df_confesiuni_jud_reg = df_confesiuni_jud_reg[confesiuni + ["Regiune"]].groupby(by="Regiune").sum()
df_confesiuni_jud_reg.to_csv("data_out/Confesiuni_reg.csv")

df_coduri_reg = pd.read_csv("data_in/Coduri_Regiuni.csv", index_col=0)
df_confesiuni_macro = df_confesiuni_jud_reg.merge(df_coduri_reg, left_index=True, right_index=True)
df_confesiuni_macro = df_confesiuni_macro[confesiuni + ["MacroRegiune"]].groupby(by="MacroRegiune").sum()
df_confesiuni_macro.to_csv("data_out/Confesiuni_macro.csv")


df_confesiuni_p = df_confesiuni[confesiuni].apply(func=lambda x:x*100/x.sum(), axis=1)

# print(df_confesiuni_p)

df_confesiuni_p.insert(0, "Localitate", df_confesiuni["City"])
df_confesiuni_p.to_csv("data_out/Confesiuni_p.csv")

df_confesiuni_jud_p = df_confesiuni_jud[confesiuni].apply(lambda x: x*100/x.sum(), axis=1)
df_confesiuni_jud_p.to_csv("data_out/Confesiuni_jud_p.csv")

df_confesiuni_reg_p = df_confesiuni_jud_reg[confesiuni].apply(lambda x: x*100/x.sum(), axis=1)
df_confesiuni_reg_p.to_csv("data_out/Confesiuni_reg_p.csv")

df_confesiuni_macro_p = df_confesiuni_macro[confesiuni].apply(lambda x: x*100/x.sum(), axis=1)
df_confesiuni_macro_p.to_csv("data_out/Confesiuni_macro_p.csv")

df_shannon = df_confesiuni_loc[confesiuni+["County"]].groupby(by="County").apply(func=shannon)
df_shannon.to_csv("data_out/shannon.csv")

df_simpson = df_confesiuni_loc[confesiuni+["County"]].groupby(by="County").apply(func=simpson)
df_simpson.to_csv("data_out/simpson.csv")

df_i_simpson = df_confesiuni_loc[confesiuni+["County"]].groupby(by="County").apply(func=inverse_simpson)
df_i_simpson.to_csv("data_out/i_simpson.csv")

df_div_jud = df_confesiuni_jud[confesiuni].apply(diversitate, axis=1)
df_div_jud.to_csv("data_out/Diversitate_jud.csv")

df_div_reg = df_confesiuni_jud_reg[confesiuni].apply(diversitate, axis=1)
df_div_reg.to_csv("data_out/Diversitate_reg.csv")
