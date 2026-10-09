import sys

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

from functii import nan_replace, standardizare, tabelare_salvare_matrice, calcul_corelatii_covariante

np.set_printoptions(precision=3, suppress=True, threshold=sys.maxsize)



df = pd.read_csv("data_in/Teritorial_2022.csv", index_col=0)
variabile = list(df)[3:]
x = df[variabile].values
# print(x, type(x), sep="\n")

# Inlocuire valori lipsa
x = nan_replace(x)
# print(x)

x_std = standardizare(x)
x_c = standardizare(x, scal=False)
tabelare_salvare_matrice(x_std, df.index, variabile, df.index.name, "x_std.csv")
tabelare_salvare_matrice(x_c, df.index, variabile, df.index.name, "x_c.csv")

# std = StandardScaler()
# x_std_ = std.fit_transform(x)
# print(x_std - x_std_)

V = np.cov(x, rowvar=False)
tabelare_salvare_matrice(V, variabile, variabile, "Indicatori", "V.csv")
R = np.corrcoef(x, rowvar=False)
tabelare_salvare_matrice(R, variabile, variabile, "Indicatori", "R.csv")
r, v, clase = calcul_corelatii_covariante(x, df["Regiunea"].values)
for i in zip(clase, r, v):
	tabelare_salvare_matrice(i[1], variabile, variabile, "Indicatori", f"R_{i[0]}.csv")
	tabelare_salvare_matrice(i[2], variabile, variabile, "Indicatori", f"V_{i[0]}.csv")
