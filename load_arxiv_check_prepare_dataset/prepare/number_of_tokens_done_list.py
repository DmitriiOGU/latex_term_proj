import pickle
import numpy as np

with open('count_list_04_04_23.pkl', 'rb') as file:
    myvar = pickle.load(file)
print(myvar[:10])
myvar = np.array(myvar)
print(len(myvar))
print(len(np.where(myvar>512))[0]*100//len(myvar))