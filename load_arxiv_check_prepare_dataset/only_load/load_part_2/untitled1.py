import os
import gzip, tarfile
# from tqdm import tqdm
list1 = os.listdir('./other files/failed')
for name1 in list1:
    name = '_'.join(name1.split('.')[:-2])
    try:
        tex = [] 
        try:
            if tarfile.is_tarfile(f"./other files/failed/{name}.tar.gz"):
                with tarfile.open(f"./other files/failed/{name}.tar.gz") as f:
                    for member in f:
                        if os.path.splitext(member.name)[1] == ".tex":
                            tex.append(f.extractfile(member).read())
            else:
                with gzip.open(f"./other files/failed/{name}.tar.gz") as f:
                    tex.append(f.read()) 
        except:
            with open("broken_Tar_gz.txt", "a") as file_exception:
                file_exception.write(f'{name} \n')
        if tex != []:
            with open (f"3/{name}_raw.txt", "wb+") as myfile:
                myfile.write(tex[0])
    except:
        with open("exceptions.txt", "a") as file_exception:
            file_exception.write(f'{name}\n')
