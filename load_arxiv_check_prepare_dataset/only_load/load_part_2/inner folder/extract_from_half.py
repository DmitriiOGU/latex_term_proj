import xml.etree.ElementTree as ET
import urllib.request as libreq
import feedparser, requests
import time, os
from pathlib import Path
import gzip, tarfile
from tqdm import tqdm
import pickle
with open('all_files_to_load_list.pkl', 'rb') as f:
    list1 = pickle.load(f)
list1 = list[170000:]
for baseurl1 in tqdm(list1):
    try:
        particles = baseurl1.split('/', maxsplit=4)[-1]
        if particles.split('/').__len__()==2:
            f_part, s_part = particles.split('/')
        else:
            f_part, s_part = particles.split('.')
        response = requests.get(baseurl1, allow_redirects=True)
        time.sleep(3.005)
        with open(f"folders/new_files/{f_part}_{s_part}.tar.gz", 'wb+') as f:
            f.write(response.content)
        tex = []
        if tarfile.is_tarfile(f"folders/new_files/{f_part}_{s_part}.tar.gz"):
            with tarfile.open(f"folders/new_files/{f_part}_{s_part}.tar.gz") as f:
                for member in f:
                    if os.path.splitext(member.name)[1] == ".tex":
                        tex.append(f.extractfile(member).read())
        else:
            with gzip.open(f"folders/new_files/{f_part}_{s_part}.tar.gz") as f:
                tex.append(f.read()) 
        if tex != []:
            with open (f"folders/new_files/{f_part}_{s_part}_raw.txt", "wb+") as myfile:
                myfile.write(tex[0])
        os.remove(f"folders/new_files/{f_part}_{s_part}.tar.gz")
        with open("all_listed_files.txt", "a") as file_exception:
            file_exception.write(baseurl1+'\n')
    except:
        print(baseurl1)
        with open("exceptions.txt", "a") as file_exception:
            file_exception.write(baseurl1+'\n')
# with open(f"folders/new_files/{k}_{f_part}_{s_part}.tar.gz", encoding="iso-8859-1") as f:
#     a = f.read().encode("utf-8").decode("utf-8")