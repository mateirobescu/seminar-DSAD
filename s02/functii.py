import pandas as pd
from pandas.core.dtypes.common import is_numeric_dtype
import numpy as np
from scipy.stats import entropy


def nan_replace_df(df: pd.DataFrame):
	for col in df.columns:
		if df[col].isna().any():
			if is_numeric_dtype(df[col]):
				df.fillna({col:df[col].mean()}, inplace=True)
			else:
				df.fillna({col:df[col].mode()}[0], inplace=True)
				
			
def shannon(df: pd.DataFrame):
	x = df.values
	tx = np.sum(x, axis=0)
	tx[tx==0] = 1
	p = x / tx
	e = entropy(p, base=2, axis=0)
	
	return pd.Series(e, index=df.columns)


def simpson(df: pd.DataFrame):
	x = df.values
	tx = np.sum(x, axis=0)
	tx[tx == 0] = 1
	p = x / tx
	s = 1 - (p**2).sum(axis=0)
	
	return pd.Series(s, index=df.columns)


def inverse_simpson(df: pd.DataFrame):
	x = df.values
	tx = np.sum(x, axis=0)
	tx[tx == 0] = 1
	p = x / tx
	tsum = (p ** 2).sum(axis=0)
	tsum[tsum == 0] = 1
	s = 1 / tsum
	
	return pd.Series(s, index=df.columns)


def diversitate(x):
	p = x / x.sum()
	h = entropy(p, base=2)
	s1 = 1 - (p * p).sum()
	s2 = 1 / (p * p).sum()
	return pd.Series([h, s1, s2], index=["Shannon", "Simpson", "InvSimpson"])
