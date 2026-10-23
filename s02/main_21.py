import pandas as pd

df_etnicitate = pd.read_csv("data_in/Ethnicity.csv", index_col=0)
etnicitati = list(df_etnicitate)[1:]

df_coduri_loc = pd.read_csv("data_in/Coduri_Localitati.csv", index_col=0)
df_coduri_jud = pd.read_csv("data_in/Coduri_Judete.csv", index_col=0)
df_coduri_reg = pd.read_csv("data_in/Coduri_Regiuni.csv", index_col=0)

df_etnicitate_loc = df_etnicitate.merge(df_coduri_loc, left_index=True, right_index=True)
df_etnicitate_jud = df_etnicitate_loc[etnicitati + ["County"]].groupby(by="County").sum()
df_etnicitate_jud.to_csv("data_out/etnicitate_jud.csv")

df_etnicitate_reg = df_etnicitate_jud.merge(df_coduri_jud, left_index=True, right_on="IndicativJudet")
df_etnicitate_reg = df_etnicitate_reg[etnicitati + ["Regiune"]].groupby(by="Regiune").sum()
df_etnicitate_reg.to_csv("data_out/etnicitate_reg.csv")

df_etnicitate_macro = df_etnicitate_reg.merge(df_coduri_reg, left_index=True, right_on="Regiune")
df_etnicitate_macro = df_etnicitate_macro[etnicitati + ["MacroRegiune"]].groupby(by="MacroRegiune").sum()
df_etnicitate_macro.to_csv("data_out/etnicitate_macro.csv")