import pandas as pd
from pandas.core.dtypes.common import is_numeric_dtype


def nan_replace_df(df: pd.DataFrame):
	for col in df.columns:
		if df[col].isna().any():
			if is_numeric_dtype(df[col]):
				df.fillna({col:df[col].mean}, inplace=True)
			else:
				df.fillna({col:df[col].mode}[0], inplace=True)