import os
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModel
import pickle
from copy import deepcopy
import re
# print(1)
tokenizer = AutoTokenizer.from_pretrained('witiko/mathberta')

def find_comment(line):
    if line[0] == '%':
        return ''
    for i in range(len(line)):
        if line[i] == '%' and line[i - 1] != '\\' : 
            return line[:i]
    return line

def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text    

def get_definitions(folder):
    replace_dict = {"\\begin\n \n{definition}": "\\begin{definition}",\
                     "\\begin \n {definition}": "\\begin{definition}",\
                     "\\begin \n{definition}": "\\begin{definition}",\
                     "\\begin\n {definition}": "\\begin{definition}",\
                     "\\begin\n{definition}": "\\begin{definition}",\
                     "\\begin {definition}": "\\begin{definition}",\
                     "\\end\n \n{definition}": "\\end{definition}",\
                     "\\end \n {definition}": "\\end{definition}",\
                     "\\end \n{definition}": "\\end{definition}",\
                     "\\end\n {definition}": "\\end{definition}",\
                     "\\end\n{definition}": "\\end{definition}",\
                     "\\end {definition}": "\\end{definition}"}
    list_of_definitions = []
    list_papers = os.listdir(folder)
    
    list_to_remove = ['0710_0044_raw.txt', '0710_0046_raw.txt',\
                      '0802_2625_raw.txt', '0804_1949_raw.txt',\
                      '0811_1367_raw.txt', '0912_1559_raw.txt',\
                      '1007_3339_raw.txt', '1010_3210_raw.txt',\
                      '1010_4450_raw.txt', '1012_5393_raw.txt',\
                      '1102_3215_raw.txt', '1104_1099_raw.txt',\
                      '1108_0519_raw.txt', '1108_5645_raw.txt',\
                      '1208_4267_raw.txt', '1211_0484_raw.txt',\
                      '1304_4847_raw.txt', '1308_4991_raw.txt',\
                      '1309_7028_raw.txt', '1310_4460_raw.txt',\
                      '1312_1868_raw.txt', '1404_5826_raw.txt',\
                      '1406_4493_raw.txt', '1505_05422_raw.txt',\
                      '1509_04023_raw.txt', '1511_02374_raw.txt',\
                      '1612_08071_raw.txt', '1701_00684_raw.txt',\
                      '1702_05292_raw.txt', '1710_02689_raw.txt',\
                      '1710_10908_raw.txt', '1712_05476_raw.txt',\
                      '1801_01328_raw.txt', '1803_08585_raw.txt',\
                      '1807_07949_raw.txt', '1807_10714_raw.txt',\
                      '1808_07633_raw.txt', '1810_00564_raw.txt',\
                      '1810_05638_raw.txt', '1901_01180_raw.txt',\
                      '1901_11316_raw.txt', '1903_03840_raw.txt',\
                      '1904_04722_raw.txt', '1907_05301_raw.txt',\
                      '2001_03940_raw.txt', '2003_05466_raw.txt',\
                      '2004_13444_raw.txt', 'math_0211459_raw.txt',\
                      'math_0410277_raw.txt', 'math_0412460_raw.txt',\
                      'math_0511129_raw.txt', 'math_0608469_raw.txt',\
                      'math_0611495_raw.txt', 'math_0612041_raw.txt',\
                      'math_9812053_raw.txt', '0705_2127_raw.txt',\
                      '0802_1323_raw.txt', '0811_1373_raw.txt',\
                      '0910_0682_raw.txt', '0912_4181_raw.txt',\
                      '1011_1679_raw.txt', '1011_4581_raw.txt',\
                      '1102_3215_raw.txt', '1105_6046_raw.txt',\
                      '1108_6330_raw.txt', '1110_1792_raw.txt',\
                      '1111_5216_raw.txt', '1206_6712_raw.txt',\
                      '1307_0150_raw.txt', '1307_7934_raw.txt',\
                      '1309_0989_raw.txt', '1310_0181_raw.txt',\
                      '1311_1577_raw.txt', '1311_2633_raw.txt',\
                      '1405_0240_raw.txt', '1407_5333_raw.txt',\
                      '1501_06534_raw.txt', '1502_04615_raw.txt',\
                      '1502_07901_raw.txt', '1503_02621_raw.txt',\
                      '1504_03762_raw.txt', '1505_01352_raw.txt',\
                      '1509_02637_raw.txt', '1509_08604_raw.txt',\
                      '1602_07132_raw.txt', '1603_02129_raw.txt',\
                      '1605_04877_raw.txt', '1606_07704_raw.txt',\
                      '1607_00852_raw.txt', '1609_08467_raw.txt',\
                      '1702_05044_raw.txt', '1702_06741_raw.txt',\
                      '1704_00990_raw.txt', '1704_03842_raw.txt',\
                      '1705_03781_raw.txt', '1706_03463_raw.txt',\
                      '1706_06145_raw.txt', '1709_01204_raw.txt',\
                      '1710_00224_raw.txt', '1710_11368_raw.txt',\
                      '1711_09295_raw.txt', '1712_02374_raw.txt',\
                      '1801_06040_raw.txt', '1806_09167_raw.txt',\
                      '1812_06246_raw.txt', '1903_00120_raw.txt',\
                      '1903_00800_raw.txt', '1904_13062_raw.txt',\
                      '1907_10656_raw.txt', '1908_02523_raw.txt',\
                      '1909_04099_raw.txt', '1912_10217_raw.txt',\
                      '2001_04424_raw.txt', '2002_10756_raw.txt',\
                      '2004_14137_raw.txt', '2004_14352_raw.txt',\
                      'math_0109189_raw.txt', 'math_0310373_raw.txt',\
                      'math_0401295_raw.txt', 'math_0506180_raw.txt',\
                      'math_0511129_raw.txt', 'math_0603390_raw.txt',\
                      'math_0608469_raw.txt', 'math_0608522_raw.txt',\
                      '1807_04717_raw.txt']
    for i in list_to_remove:
        if i in list_papers:
            list_papers.remove(i)
    for i in tqdm(list_papers):  
        with open(folder + '/' + i, 'r') as f:
            try:
                text_itself = f.read()
                text_itself = text_itself.split('\n')
                text_itself = [find_comment(j) if '%' in j else j for j in text_itself]
                text_itself = '\n'.join(text_itself)
                text_itself = re.sub(r' +', ' ', text_itself)
                text_itself = re.sub(r'\n+','\n', text_itself)
                text_itself = replace_all(text_itself, replace_dict)
                if '\\begin{definition}' in text_itself:
                        # print(i)
                        start = text_itself.find('\\begin{definition}')
                        end = text_itself.find('\\end{definition}') + 16
                        while start != -1 and end != 15:
                            
                            
                            if text_itself[start:end] == '':
                                print(i, start, end)
                            while '\\begin{definition}' in text_itself[start+18: end - 16]:
                                inner_start = text_itself[start+18: end - 16].find('\\begin{definition}')
                                # list_of_definitions.append(text_itself[inner_start+start+18:end])
                                text_itself = text_itself[:start + 18 + inner_start] + text_itself[end:]
                                end = text_itself.find('\\end{definition}') + 16
                            # if start>1000:
                            #     slice_start = start-1000
                            # else:
                            #     slice_start = 0
                            # next_definition = text_itself[end:].find('\\begin{definition}')
                            # slice_end = end + 16 + 1000
                            # if next_definition != -1:
                            #     if slice_end > next_definition + end:
                            #         slice_end = next_definition + end
                            # list_of_definitions.append(text_itself[start:end])
                            text_itself = text_itself[:start] + text_itself[end:]
                            
                            start = text_itself.find('\\begin{definition}')
                            end = text_itself.find('\\end{definition}') + 16

                list_of_definitions.append(text_itself)
            except:
                pass
    return list_of_definitions

list_of_definitions = []
list_of_definitions += get_definitions('./first_part')
list_of_definitions += get_definitions('./second_part/1')
list_of_definitions += get_definitions('./second_part/2')
# list_of_definitions = list_of_definitions[:100000]

# for i in tqdm(list_of_definitions):
#     count_list.append(tokenizer(i)['input_ids'].__len__())
with open('neg_examples_06_04.pkl', 'wb') as file:
    pickle.dump(list_of_definitions, file)
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
    
              
