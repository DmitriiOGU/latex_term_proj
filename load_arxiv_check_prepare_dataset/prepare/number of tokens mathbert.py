import os
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModel
import pickle
# print(1)
tokenizer = AutoTokenizer.from_pretrained('witiko/mathberta')
# print(os.listdir('./first_part'))
list_of_definitions = []
def get_definitions(folder):
    list_of_definitions = []
    list_papers = os.listdir(folder)
    for i in tqdm(list_papers):  
        with open(folder + '/' + i, 'r') as f:
            try:
                a = f.read()
                if '\\begin{definition}' in a:
                        start = a.find('\\begin{definition}')+18
                        while start!=17:
                            end = a.index('\\end{definition}')
                            if end == -1:
                                break
                            list_of_definitions.append(a[start:end])
                            a = a[end+16:]
                            start = a.index('\\begin{definition}')+18
            except:
                pass
    return list_of_definitions
list_of_definitions += get_definitions('./first_part')
list_of_definitions += get_definitions('./second_part/1')
list_of_definitions += get_definitions('./second_part/2')
# list_of_definitions = list_of_definitions[:100000]
count_list = []
for i in tqdm(list_of_definitions):
    count_list.append(tokenizer(i)['input_ids'].__len__())
with open('count_list_04_04_23.pkl', 'wb') as file:
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
    
              