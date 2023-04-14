import os
import pickle
from lxml import etree as ET

def exchange_naming(base_addr):
    if base_addr.split('/').__len__() == 2:
        f_part, s_part = base_addr.split('/')
    else:
        f_part, s_part = base_addr.split('.')
    return('_'.join([f_part, s_part]))
def get_attr(xml, attributes):
   for child in (xml[:1]):
       if len(child.attrib)!= 0:
           attributes.append(child.attrib)
       get_attr(child,attributes)
   return attributes


files_list = ['./first_part', './second_part/1', './second_part/2']
supervisor_list = []
for directory in files_list:
    supervisor_list.append(list(map(lambda x: x[:-8], os.listdir(directory))))

for file_xml in os.listdir('./xml_files/')[:1]:
    # print(file_xml)
    tree = ET.parse(f'./xml_files/{file_xml}')
    root = tree.getroot()
    for child in root[:2]:
        print(child.attrib['name'].split('/')[1].split('.'))
        # f_part, s_part = child.attrib['name'].split('/')[1].split('.')
        for definition in child:
            for
            
       