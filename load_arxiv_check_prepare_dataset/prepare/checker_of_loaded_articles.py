import os
import pickle
def exchange_naming(base_addr):
    if base_addr.split('/').__len__() == 2:
        f_part, s_part = base_addr.split('/')
    else:
        f_part, s_part = base_addr.split('.')
    return('_'.join([f_part, s_part]))
files_list = ['./first_part', './second_part/1', './second_part/2']
a = set()
for directory in files_list:
    a.update(list(map(lambda x: x[:-8], os.listdir(directory))))
with open('all_files_to_load_list.pkl', 'rb') as f:
    list1 = pickle.load(f)
list1 = set(list(map(exchange_naming, list1)))
result = list1 - a
with open(f"woudlnt_achieved_papers.txt", 'w') as f:
    for i in result:
        f.write(i + '\n')