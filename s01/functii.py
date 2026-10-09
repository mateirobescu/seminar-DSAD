import numpy as np
import pandas as pd


# Inlocuire valori lipsa cu media pe coloane
def nan_replace(x: np.ndarray):
	x = x.copy()
	k = np.where(np.isnan(x))
	x[k] = np.nanmean(x[:, k[1]], axis=0)
	return x


# Centrare/Standardizare
def standardizare(x: np.ndarray, scal = True, nlib = 0):
	x_ = x - np.mean(x, axis=0)
	if scal:
		x_ = x_ / np.std(x_, axis=0, ddof=nlib)
	return x_


def tabelare_salvare_matrice(x: np.ndarray, index_linie, index_coloana, nume_index, nume_fisier=None):
	df = pd.DataFrame(x, index=index_linie, columns=index_coloana)
	df.index.name = nume_index
	if nume_fisier is not None:
		df.to_csv(f"data_out/{nume_fisier}")
		

def calcul_corelatii_covariante(x: np.ndarray, y: np.ndarray):
	clase = np.unique(y)
	q = len(clase)
	m = x.shape[1]
	r = np.empty((q,m,m))
	v = np.empty((q,m,m))
	for i in range(q):
		z = x[y==clase[i], :]
		r[i] = np.corrcoef(z, rowvar=False)
		v[i] = np.cov(z, rowvar=False)
	return r, v, clase

