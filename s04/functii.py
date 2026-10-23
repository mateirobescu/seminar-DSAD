import numpy as np
import pandas as pd
from pandas.core.dtypes.common import is_numeric_dtype


def nan_replace_df(df: pd.DataFrame):
	for col in df.columns:
		if df[col].isna().any():
			if is_numeric_dtype(df[col]):
				df.fillna({col:df[col].mean()}, inplace=True)
			else:
				df.fillna({col:df[col].mode()}[0], inplace=True)


def acp(x: np.ndarray, std=True, nlib=0):
	n,m = x.shape
	x_ = x - np.mean(x, axis=0)
	if std:
		x_ = x_ / np.std(x_, axis=0)
	r_v = (1/(n-nlib))*x_.T@x_
	valp, vecp = np.linalg.eig(r_v)
	valp = np.real(valp)
	vecp = np.real(vecp)
	k = np.flip(np.argsort(valp))
	alpha = valp[k]
	a = vecp[:,k]
	c = x_@a
	return x_, r_v,alpha,a,c


def tabelare_varianta(alpha:np.ndarray):
	procent = alpha*100/sum(alpha)
	df = pd.DataFrame(
		{
			"Varianta": alpha,
			"Varianta cumulata": np.cumsum(alpha),
			"Procent varianta": procent,
			"Procnet cumulat": np.cumsum(procent)
		}, ["C" + str(i+1)]
	)
	
	
	