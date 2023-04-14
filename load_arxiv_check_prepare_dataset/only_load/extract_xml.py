import xml.etree.ElementTree as ET
import urllib.request as libreq
import feedparser, requests
import time, os
from pathlib import Path
import gzip, tarfile
from tqdm import tqdm
import pickle
# list1 = []
# for file_xml in os.listdir('./folders/xml_files/'):
#     # print(file_xml)
#     tree = ET.parse(f'./folders/xml_files/{file_xml}')
#     root = tree.getroot()
#     for child in root:
#         # print(child.attrib['name'].split('/')[1].split('.'))
#         f_part, s_part = child.attrib['name'].split('/')[1].split('.')
#         if f_part in ['math', 'math-ph', 'physics']:
#             baseurl1 = f'https://arxiv.org/e-print/{f_part}/{s_part}'
#         else:
#             baseurl1 = f'https://arxiv.org/e-print/{f_part}.{s_part}'
#         list1.append(baseurl1)
# list1 = list(set(list1))
# with open('all_files_to_load_list.pkl', 'wb') as f:
#     pickle.dump(list1, f)
with open('all_files_to_load_list.pkl', 'rb') as f:
    list1 = pickle.load(f)
list1 = list1[41197+31000:]
2
for base_addr in tqdm(list1):
    if base_addr.split('/').__len__() == 2:
        f_part, s_part = base_addr.split('/')
    else:
        f_part, s_part = base_addr.split('.')
    baseurl1 = 'https://export.arxiv.org/e-print/'+base_addr
    try:
       
        response = requests.get(baseurl1, allow_redirects=True)
        time.sleep(1.005)
        with open(f"folders/new_files/{f_part}_{s_part}.tar.gz", 'wb+') as f:
            f.write(response.content)
        tex = []
        try:
            if tarfile.is_tarfile(f"folders/new_files/{f_part}_{s_part}.tar.gz"):
                with tarfile.open(f"folders/new_files/{f_part}_{s_part}.tar.gz") as f:
                    for member in f:
                        if os.path.splitext(member.name)[1] == ".tex":
                            tex.append(f.extractfile(member).read())
            else:
                with gzip.open(f"folders/new_files/{f_part}_{s_part}.tar.gz") as f:
                    tex.append(f.read()) 
        except:
            with open("broken_Tar_gz.txt", "a") as file_exception:
                file_exception.write(baseurl1+'\n')
        if tex != []:
            with open (f"folders/new_files/{f_part}_{s_part}_raw.txt", "wb+") as myfile:
                myfile.write(tex[0])
        else:
            with open (f"folders/new_files/{f_part}_{s_part}_raw.txt", "wb+") as myfile:
                myfile.write(response.content)
        os.remove(f"folders/new_files/{f_part}_{s_part}.tar.gz")
        with open("all_listed_files.txt", "a") as file_exception:
            file_exception.write(baseurl1+'\n')
    except:
        print(baseurl1)
        with open("exceptions.txt", "a") as file_exception:
            file_exception.write(baseurl1+'\n')
# with open(f"folders/new_files/{k}_{f_part}_{s_part}.tar.gz", encoding="iso-8859-1") as f:
#     a = f.read().encode("utf-8").decode("utf-8")