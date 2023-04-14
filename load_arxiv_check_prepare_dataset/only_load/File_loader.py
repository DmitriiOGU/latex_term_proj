# -*- coding: utf-8 -*-
import urllib.request as libreq
import feedparser, requests
import time, os
from pathlib import Path
import gzip, tarfile
#from Parser_of_file import Parser_of_file
# from plasTeX.TeX import TeX
# from plasTeX.Renderers.XHTML import Renderer
from Parser_of_file  import Parser_of_file  
from tqdm import tqdm

class File_loader:
    def __init__(self, search_query:str='all:math.AG', start:int=0, max_results:int=1, download_folder='./download', prefix=str(0)+'_'):
        """
        Parameters
        ----------
        search_query : str, optional
            DESCRIPTION. The default is 'all:math.AG', need for parsing arxiv.org
        start : int, optional
            DESCRIPTION. The default is 0, need for parsing arxiv.org
        max_results : int, optional
            DESCRIPTION. The default is 1, need for parsing arxiv.org
        """
        self.text_list = self.initialize_list_of_tetxts(search_query, start, max_results, download_folder, prefix)
        
    def initialize_list_of_tetxts(self, search_query, start, max_results, download_folder, prefix):
        """
        Parameters
        ----------
        search_query : str
            query for arxiv api
        start : int
            start of arxiv_num
        max_results : int
            number of query results
        Returns
        -------
        list_of_tetxts : list of sentences
            DESCRIPTION.
        """
        list_of_tetxts = []
        # Base api query url
        base_url = 'http://export.arxiv.org/api/query?'
        query = f'search_query={search_query}&start={start}&max_results={max_results}&sortOrder=ascending'
        Path(download_folder).mkdir(parents=True, exist_ok=True)
        counter_of_file = 0
        with  libreq.urlopen(base_url+query) as get_all:
            feed = feedparser.parse(get_all.read())
            time.sleep(3.005)
            print(feed.entries.__len__())
            for entry in feed.entries:
                try: 
                    hidden =[]
                    baseurl1 = 'https://arxiv.org/e-print/'+entry.id.split('/abs/')[-1]
                    response = requests.get(baseurl1, allow_redirects=True)
                    time.sleep(3.005)
                    with open(download_folder+f"/{prefix}1.tar.gz", 'wb+') as f:
                            f.write(response.content)
                    # print(response.content)
                    tex = []
                    if tarfile.is_tarfile(download_folder + f"/{prefix}1.tar.gz"):
                        with tarfile.open(download_folder + f"/{prefix}1.tar.gz") as f:
                            for member in f:
                                if os.path.splitext(member.name)[1] == ".tex":
                                    tex.append(f.extractfile(member).read())
                    else:
                        with gzip.open(download_folder + f"/{prefix}1.tar.gz") as f:
                            tex.append(f.read()) 
                    if tex != []:
                        with open (download_folder + f"/{prefix}raw"+str(counter_of_file)+".txt", "wb+") as myfile:
                            myfile.write(tex[0])
                            # print(tex[0])
                        with open (download_folder + f"/{prefix}"+str(counter_of_file)+".tex", "r") as myfile:
                            #"download\\raw0.tex"
                            hidden = Parser_of_file(myfile.readlines()).get_sentences()
                except Exception as e:
                    #print(e)
                    # print(tex)
                    pass
                if hidden or hidden!=[]:
                    list_of_tetxts += hidden
                counter_of_file += 1
                time.sleep(3.005)
        my_zip_file =  Path(download_folder + f"/{prefix}1.tar.gz")
        if my_zip_file.exists():
            os.remove(download_folder + f"/{prefix}1.tar.gz")
        return list_of_tetxts
    
    def get_text_list(self):
        return self.text_list