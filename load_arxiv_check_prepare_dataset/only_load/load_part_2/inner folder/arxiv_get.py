import os
from time import sleep
from pathlib import Path
from tqdm import tqdm
from typing import List
from urllib.request import urlretrieve
from enum import Enum
from subprocess import call

FileStatus = Enum('FileStatus',['VERIFIED', 'FAILED', 'DOWNLOADED', 'ABSENT'])

folders = {
    FileStatus.VERIFIED: Path('verified'),
    FileStatus.FAILED: Path('failed'),
    FileStatus.DOWNLOADED: Path('downloaded'),
}
   

def tgz_ok(path: str) -> bool:
    return call(f'bash -c "gzip -t {path}"',shell=True)==0

class ArxivArticle:
    arxiv_id:str
    status:FileStatus
    
    def __init__(self, identifier:str)->None:
        self.arxiv_id = identifier
        self.update_info()


    def get_filename(self) -> Path:
        return Path(self.arxiv_id.strip()
               .replace('/','_').replace('.','_') 
               +'.tar.gz')
        
    def get_status(self) -> FileStatus:
        for key, value in folders.items():
            if (value / self.filename).is_file():
                return key
        else:
            return FileStatus.ABSENT
    
    def update_info(self)->None:
        self.filename = self.get_filename()
        self.status = self.get_status()
    
    
            
    def set_status(self, status:FileStatus)->None:
        if status != self.status and status!=FileStatus.ABSENT:
            origin = folders[self.status] / self.filename
            destination = folders[status] / self.filename
            origin.replace(destination)
            self.update_info()
    
    def download(self, log_stream)->bool:
        try:
            urlretrieve('https://export.arxiv.org/e-print/'+self.arxiv_id, 
                        folder[FileStatus.DOWNLOADED] / self.filename)
        except Exception as e:
            log_retrieve.write(f"Failed to download {i}: {str(e)}\n")
            return False
        return True


    
def verify_ids(ids:List[ArxivArticle]) -> None:
    os.makedirs(folders[FileStatus.VERIFIED], exist_ok=True)
    os.makedirs(folders[FileStatus.FAILED], exist_ok=True)
    for i in tqdm(ids):
        if i.status != FileStatus.DOWNLOADED:
            continue
        if tgz_ok(folders[i.status] / i.filename):
            i.set_status(FileStatus.VERIFIED)
        else:
            i.set_status(FileStatus.FAILED)

      
def download_ids(ids:List[ArxivArticle]) -> None:
    logfile = 'exceptions.log'
    os.makedirs(folders[FileStatus.DOWNLOADED], exist_ok=True)
    batch_size = 0
    log_retrieve = open(logfile,'a')
    for i in tqdm(ids):
        if i.status != FileStatus.ABSENT:
            continue
        success = i.download(log_retrieve)
        if success:
            batch_size+=1
        if (batch_size>3):
            sleep(1.01)
            batch_size=0
    log_retrieve.close()

def write_status_lists(ids:List[ArxivArticle]) -> None:
    files = {}
    files[FileStatus.ABSENT] = open('absent.txt','w')
    files[FileStatus.VERIFIED] = open('verified.txt','w')
    files[FileStatus.DOWNLOADED] = open('downloaded.txt','w')
    files[FileStatus.FAILED] = open('failed.txt','w')
    for i in ids:
        files[i.status].write(i.arxiv_id)
    for f in files.values():
        f.close()

if __name__ == "__main__":
    with open('ids.txt', 'r') as f:
        ids = f.readlines()
    ids = [ArxivArticle(i) for i in ids[170000:]]
    print('ids list loaded')
    #ids = ids[-2:]
    #download_ids(ids)
    #verify_ids(ids)
    write_status_lists(ids)
    