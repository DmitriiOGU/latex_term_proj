import pickle
import pandas as pd

with open('list_of_def_stat_04_04_23.pkl', 'rb') as file:
    cl = pickle.load(file)

df = pd.Series(cl)
df.plot.hist(bins=100)