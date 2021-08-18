import xml.etree.ElementTree as ET
from os import getcwd
import os

# sets=[('2007', 'train'), ('2007', 'val'), ('2007', 'test')]
# sets=[('2007', 'train'), ('2007', 'val')]

# classes = ["0", "1", "2", "3", "4", "5", "6", "7"]
faceclas = ["face", "face_mask"]

path = './test_xml/'  #待检测图片xml的位置

truth_path = './truth'
if not os.path.exists(truth_path):
    os.makedirs(truth_path)

# truth如果之前存放的有文件，全部清除
for i in os.listdir(truth_path):
    path_file = os.path.join(truth_path,i)
    if os.path.isfile(path_file):
        os.remove(path_file)


def convert_annotation(file, xml_path):
    in_file = open(xml_path)
    tree=ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in faceclas or int(difficult)==1:
            continue
        if cls == "face":
            cls = 'no_mask'
        elif cls =="face_mask":
            cls = 'have_mask'
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        file.write(cls +' ' +" ".join([str(a) for a in b])+'\n')

wd = getcwd()

# for year, image_set in sets:
#     image_ids = open('VOCdevkit/VOC%s/ImageSets/Main/%s.txt'%(year, image_set)).read().strip().split()
#     list_file = open('%s_%s.txt'%(year, image_set), 'w')
#     for image_id in image_ids:
#         list_file.write('%s/VOCdevkit/VOC%s/JPEGImages/%s.jpg'%(wd, year, image_id))
#         convert_annotation(year, image_id, list_file)
#         list_file.write('\n')
#     list_file.close()
for filename in os.listdir(path):
    xml_path = path + '/' + filename
    portion = os.path.split(xml_path)
    name = os.path.splitext(portion[1])
    txt_path = truth_path + '/' + name[0] + '.txt'
    file = open(txt_path, 'w')
    convert_annotation(file, xml_path)
    file.close()