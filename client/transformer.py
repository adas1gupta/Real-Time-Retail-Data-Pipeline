import numpy as np
from numpy import add
import pandas as pd

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
df = pd.read_excel(url)
df['json'] = df.to_json(orient='records', lines=True).splitlines()
dfjson = df['json']
np.savetxt(r'./output.txt', dfjson.values, fmt='%s')