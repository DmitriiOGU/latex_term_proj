import os
from time import sleep
from pathlib import Path
from tqdm import tqdm
from typing import List
from urllib.request import urlretrieve
from enum import Enum


def grouper(l:List[str], size:int=4) -> List[List[str]]:
    return  [l[i:i+size] for i in range(0, len(l), size)]

FileStatus = Enum('FileStatus',['VERIFIED', 'FAILED', 'DOWNLOADED', 'ABSENT'])

folder = {
    FileStatus.VERIFIED: Path('verified'),
    FileStatus.FAILED: Path('failed'),
    FileStatus.DOWNLOADED: Path('downloaded'),
    #FileStatus.ABSENT: None,
}

def id_filename(id:str)->Path:
    return Path(i.strip().replace('/','_').replace('.','_') +'.tar.gz')

def status(arxiv_id:str) -> FileStatus:
    filename = id_filename(arxiv_id)
    for key, value in folder.items():
        if (value / filename).is_file():
            return key
    else:
        return FileStatus.ABSENT
    
    

def get_ids(ids:List[str], logfile:str)->None:
    batch_size = 0
    log_retrieve = open(logfile,'a')
    for i in tqdm(ids):
        if status(i) != FileStatus.ABSENT:
            continue
        try:
            urlretrieve('https://export.arxiv.org/e-print/'+i, 
                        folder[FileStatus.DOWNLOADED] / id_filename(i))
        except Exception as e:
            log_retrieve.write(f"Failed to download {i}: {str(e)}\n")
        batch_size+=1
        if (batch_size>3):
            sleep(1.01)
            batch_size=0
    log_retrieve.close()


def download(ids:List[str]) -> None:
    logfile = 'exceptions.log'
    os.makedirs(folder[FileStatus.DOWNLOADED], exist_ok=True)
    get_ids(ids, logfile)

def move(filename: str, origin_folder: Path, destination_folder: Path)->None:
    pass

def verify(ids:List[str]) -> None:
    os.makedirs(folder[FileStatus.VERIFIED], exist_ok=True)
    os.makedirs(folder[FileStatus.FAILED], exist_ok=True)
    for i in ids:
      if 

if __name__ == "__main__":
    with open('ids.txt', 'r') as f:
        ids = f.readlines()
    ids = ids[170000:]
    #download(ids)
    #verify(ids)
    