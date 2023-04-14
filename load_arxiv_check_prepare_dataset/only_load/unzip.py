import gzip
import os
import shutil
k = 0
folder = 'SGD.v3'
for i in os.listdir(folder):
    for j in os.listdir(f'{folder}/{i}'):
        with gzip.open(f'{folder}/{i}/{j}', 'rb') as f_in:
            with open(f'xml_files/{k}.xml', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        k+=1  
folder = 'NN.v1'
for i in os.listdir(folder):
    for j in os.listdir(f'{folder}/{i}'):
        with gzip.open(f'{folder}/{i}/{j}', 'rb') as f_in:
            with open(f'xml_files/{k}.xml', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        k+=1    