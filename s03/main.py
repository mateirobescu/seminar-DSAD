import pandas as pd
from numpy.ma.extras import average


def calcul_medie(df:pd.DataFrame):
    x = df.values
    medii = average(x[:,:-1],axis=0,weights=x[:,-1])
    return pd.Series(medii,df.columns[:-1])


pd.set_option('display.max_columns', None)

df_industrie_alim = pd.read_csv("data_in/IndustriaAlimentara.csv", index_col=0)
activitati = list(df_industrie_alim.columns.values)[1:]


# 1
s_totaluri = df_industrie_alim[activitati].sum(axis=1)
# print(s_totaluri)
df_cerinta1 = df_industrie_alim[s_totaluri > 0]
df_cerinta1.to_csv("data_out/Cerinta1.csv")

# 2
df_industrie_alim["Total"] = s_totaluri
df_cerinta2 = df_industrie_alim[activitati].apply(
    func = lambda x: x/x.sum() ,
    axis = 1
)
df_cerinta2.insert(0,"Localitate",df_industrie_alim["Localitate"])
# print(df_cerinta2.head(3))
df_cerinta2.to_csv("data_out/Cerinta2.csv")

# 3
df_populatie = pd.read_csv("data_in/PopulatieLocalitati.csv", index_col=0)
df_industrie_alim_loc = df_industrie_alim.merge(
    df_populatie[["Judet","Populatie"]],
    left_index=True,
    right_index=True)
s_cerinta3 = df_industrie_alim_loc["Total"]/df_industrie_alim_loc["Populatie"]
s_cerinta3.name = "Pondere"
s_cerinta3.round(5).to_csv("data_out/Cerinta3.csv")

# 4
df_industrie_alim_jud = df_industrie_alim_loc[activitati+["Judet","Populatie"]].groupby(by="Judet").sum()
# print(df_industrie_alim_jud.head(3))
s_cerinta4 = df_industrie_alim_jud[activitati].apply(
    lambda x:x.index[x.argmax()],
    axis = 1
)
s_cerinta4.name="Activitate"
s_cerinta4.to_csv("data_out/Cerinta4.csv")

# 5
df_coduri = pd.read_csv("data_in/Coduri_Judete.csv", index_col=0)
df_industrie_alim_loc_reg = df_industrie_alim_loc.merge(
    df_coduri,
    left_on="Judet",
    right_index=True
)
# print(df_industrie_alim_loc_reg.head(3))
df_cerinta5 = df_industrie_alim_loc_reg[activitati+["Regiune","Populatie"]].groupby(by="Regiune").apply(
    func=calcul_medie,
    include_groups=False
)
df_cerinta5.to_csv("data_out/Cerinta5.csv")
