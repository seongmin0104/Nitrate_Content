import xml.etree.ElementTree as ET
import os
path = 'C:/Users/Always9/Desktop/Labeling Image/[new]1_drosophila_suzukii-20180425T100628Z-001/[new]1_drosophila_suzukii'
list_path = os.listdir(path)
list_xml = [x for x in list_path if x[16:19] == 'xml']
path = 'C:/Users/Always9/Desktop/Labeling Image/[new]1_drosophila_suzukii-20180425T100628Z-001/[new]1_drosophila_suzukii/'
b = []
for filename in list_xml:
    tree = ET.parse(path+filename)
    root = tree.getroot()
    a = []
    for child in root:
        a.append(child.tag)
    b.append(a.count('object'))
print(sum(b))

