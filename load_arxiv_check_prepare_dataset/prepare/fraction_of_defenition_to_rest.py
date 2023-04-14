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
                text_itself = f.read()
                text_itself = replace_all(text_itself, replace_dict)
                text_copy = deepcopy(text_itself)
                count_definitions = 0
                if '\\begin { definition } ' in text_itself:
                        # print(i)
                        start = text_itself.find('\\begin { definition } ')+22
                        end = text_itself.find('\\end { definition } ')
                        while start != 23 and end != -1:
                            count_definitions += tokenizer(text_itself[start:end])['input_ids'].__len__()
                            # list_of_definitions.append(text_itself[start:end])
                            text_itself = text_itself[end + 20:]
                            start = text_itself.find('\\begin { definition } ')+22
                            end = text_itself.find('\\end { definition } ')
                if count_definitions>0:
                    count_all = tokenizer(text_copy)['input_ids'].__len__()
                    # print(count_all, count_definitions)
                    count_list.append(count_definitions/count_all)
            except:
                pass
    return count_list

count_list = []
count_list += get_definitions('./first_part')
count_list += get_definitions('./second_part/1')
count_list += get_definitions('./second_part/2')
# list_of_definitions = list_of_definitions[:100000]

# for i in tqdm(list_of_definitions):
#     count_list.append(tokenizer(i)['input_ids'].__len__())
with open('list_of_def_stat_04_04_23.pkl', 'wb') as file:
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
    
              
