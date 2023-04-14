
def start_end_find(type_of:str, start_end:int, text_itself:str,) -> int:
    if type_of == 'start':
        length_of_term = 18
        modifier = 0
        text = '\\begin{definition}'
    elif type_of == 'end':
        length_of_term = 16
        modifier = 16
        text = '\\end{definition}'
    else:
        print('Wrong type of function')
        return 
    begin_line_def = text_itself[text_itself[:start_end].rfind('\n') + 1: start_end]
    copy_text = text_itself
    counter = 0
    print(begin_line_def)
    while not(sum([0 if i=='%' or i==' ' else 1 for i in begin_line_def])) and begin_line_def != '':
        # если нулик то обрезаем по конец строчки, если 1, то считаем стартом, надо запихнуть в суб функцию
        counter += start + length_of_term
        copy_text = copy_text[start + length_of_term:]
        start_end = copy_text.find(text)
        begin_line_def = copy_text[copy_text[:start_end].rfind('\n') + 1: start_end]
    start_end += counter + modifier
    return start_end
def find_comment(line):
    if line[0] == '%':
        return ''
    for i in range(len(line)):
        if line[i] == '%' and line[i - 1] != '\\' : 
            return line[:i]
    return line
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

import re
def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text    
list_of_definitions = []
with open('first_part/1807_04717_raw.txt', 'r') as f:
        text_itself = f.read()
        text_itself = text_itself.split('\n')
        for i in range(len(text_itself)):
            if '%' in text_itself[i]:
                text_itself[i] = find_comment(text_itself[i])
        text_itself = '\n'.join(text_itself)
        text_itself = re.sub(r' +', ' ', text_itself)
        text_itself = re.sub(r'\n+','\n', text_itself)
        text_itself = replace_all(text_itself, replace_dict)
        if '\\begin{definition}' in text_itself:
                
                # iffalse fi
                start = text_itself.find('\\begin{definition}')
                #вырез строки c \n  до позиции начала '\\begin{definition}' 
                # 26 definitions Должно быть 24
                # start = start_end_find("start", start, text_itself)
                #повторить для конечной функции
                end = text_itself.find('\\end{definition}')+16
                # end = start_end_find("end", end, text_itself)
                while start != -1 and end != 15:
                    # if start>1000:
                    #     slice_start = start-1000
                    # else:
                    #     slice_start = 0
                    next_definition = text_itself[end:].find('\\begin{definition}')
                    slice_end = end + 16 + 1000
                    # if next_definition != -1:
                    #     if slice_end>next_definition:
                    #         slice_end = next_definition
                    while '\\begin{definition}' in text_itself[start+18: end - 16]:
                        inner_start = text_itself[start+18: end - 16].find('\\begin{definition}')
                        list_of_definitions.append(text_itself[inner_start+start+18:end])
                        text_itself = text_itself[:start + 18 + inner_start] + text_itself[end:]
                        end = text_itself.find('\\end{definition}') + 16
                    # print(start, end)
                    list_of_definitions.append(text_itself[start:end])
                    text_itself = text_itself[end:]
                    start = text_itself.find('\\begin{definition}')
                    # start = start_end_find("start", start, text_itself)
                    end = text_itself.find('\\end{definition}') + 16
                    # end = start_end_find("end", end, text_itself)