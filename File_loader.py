# -*- coding: utf-8 -*-
import urllib.request as libreq
import feedparser, requests
import time, os
from pathlib import Path
import gzip, tarfile
from Parser_of_file import Parser_of_file

class File_loader:
    def __init__(self, search_query:str='all:math.AG', start:int=0, max_results:int=1):
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
        self.text_list = self.initialize_list_of_tetxts(search_query, start, max_results)
        
    def initialize_list_of_tetxts(self, search_query, start, max_results):
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
        base_url = 'http://export.arxiv.org/api/query?';        
        query = f'search_query={search_query}&start={start}&max_results={max_results}'
        Path("download").mkdir(parents=True, exist_ok=True)
        with  libreq.urlopen(base_url+query) as get_all:
            feed = feedparser.parse(get_all.read())
            time.sleep(4)
            for entry in feed.entries:
                try: 
                    hidden =[]
                    baseurl1 = 'https://arxiv.org/e-print/'+entry.id.split('/abs/')[-1]
                    response = requests.get(baseurl1, allow_redirects=True)
                    with open("download/1.tar.gz", 'wb+') as f:
                            f.write(response.content)
                    tex = []
                    if tarfile.is_tarfile("download\\1.tar.gz"):
                        with tarfile.open("download\\1.tar.gz") as f:
                            for member in f:
                                if os.path.splitext(member.name)[1] == ".tex":
                                    tex.append(f.extractfile(member).read())
                    else:
                        with gzip.open("download\\1.tar.gz") as f:
                            tex.append(f.read()) 
                    if tex != []:
                        with open ("download\\raw.txt", "wb+") as myfile:
                            myfile.write(tex[0])
                            # print(tex[0])
                        with open ("download\\raw.txt", "r") as myfile:
                            hidden = Parser_of_file(myfile.readlines()).get_sentences()
                except Exception as e:
                    #print(e)
                    # print(tex)
                    pass
                if hidden or hidden!=[]:
                    list_of_tetxts += hidden
                time.sleep(3)
        #shutil.rmtree("download")
        return list_of_tetxts
    
    def get_text_list(self):
        return self.text_list