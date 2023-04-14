import os
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModel
import pickle
from copy import deepcopy
# print(1)
tokenizer = AutoTokenizer.from_pretrained('witiko/mathberta')
# print(os.listdir('./first_part'))
replace_dict = {"{": " { ",\
                "}": " } ",\
                "[": " [ ",\
                "]": " ] ",\
                "(": " ( ",\
                ")": " ) ",\
                "$": " $ "}

replace_dict1 = {"[": " [ ",\
                "]": " ] ",\
                "(": " ( ",\
                ")": " ) ",\
                "$": " $ "}


def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j).replace("  ", " ")
    return text

def get_definitions(folder):
    count_list = []
    list_of_definitions = []
    list_papers = os.listdir(folder)
    for i in tqdm(list_papers):  
        with open(folder + '/' + i, 'r') as f:
            try:
                a= f.read()
                a = replace_all(a, replace_dict)
                length = len(a)
                if length//1000*1000<length:
                    iteration = length//1000
                else:
                    iteration = length//1000+1
                for j in range(iteration):
                    count_list.append(tokenizer(a[1000*j:1000*(j+1)])['input_ids'].__len__())
            except:
                pass
    return count_list

count_list = []
count_list += get_definitions('./first_part')
# count_list += get_definitions('./second_part/1')
# count_list += get_definitions('./second_part/2')
# list_of_definitions = list_of_definitions[:100000]

# for i in tqdm(list_of_definitions):
#     count_list.append(tokenizer(i)['input_ids'].__len__())
with open('number_of_tokes_06_04.pkl', 'wb') as file:
    pickle.dump(count_list, file)
# with open('./first_part/0704_0022_raw.txt', 'r') as f:
#     a = f.read()
#     start = a.find('\\begin{definition}')+18
#     while start!=-17:
#         end = a.index('\\end{definition}')
#         if end == -1:
#             break
#         list_of_definitions.append(a[start:end])
#         a = a[end+16:]
#         start = a.index('\\begin{definition}')+18
    
              
