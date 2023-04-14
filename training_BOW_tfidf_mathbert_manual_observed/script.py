# -*- coding: utf-8 -*-
#импрот библиотек
import json
import pandas as pd
import apyori 
from io import StringIO
from File_loader import File_loader

#parse latex
# for file in os.listdir():
#     if file.endswith(".tex"):
#         name_of_file=file
# with open (name_of_file, "r") as myfile:
#     parser = Parser_of_file(myfile.readlines())
#     data = parser.get_sentences()
def main():
    data = File_loader(max_results=1000).get_text_list()
    data = list(filter(None, data))
    results = list(apyori.apriori(data, min_support=0.0005))
    output = []
    for RelationRecord in results:
        o = StringIO()
        apyori.dump_as_json(RelationRecord, o)
        output.append(json.loads(o.getvalue()))
    data_df = pd.DataFrame(output)
    # и взгялнем на итоги
    pd.set_option('display.max_colwidth', -1)
    with open('Failed.html', 'w') as file:
        file.write(data_df.to_html())
if __name__ == '__main__':
    main()