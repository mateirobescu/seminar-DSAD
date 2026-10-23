import sys
import numpy as np
import pandas as pd

from s04.functii import nan_replace_df, acp

np.set_printoptions(suppress=True, precision=5, threshold=sys.maxsize)

df = pd.read_csv("data_in/ConsumAlimentar/ConsumAlimentar.csv", index_col=1)

if df.isna().any().any():
	nan_replace_df(df)
	
	
variabile_observate = list(df)[1:]
x = df[variabile_observate].values
x_, r_v, alpha, a, c = acp(x)

# Analiza variantei componentelor
# Tabelarea variantei




