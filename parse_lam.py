# -*- coding: utf-8 -*-
"""
Created on Tue Sep  12 20:50:10 2023

@author: Lincoln Scheer
            
"""

import xml.etree.ElementTree as ET
from pathlib import Path
import shutil
import os

# See bottom of script to run

# Rest Of Scrpt ###############################################################

# Parses bounding bound objects from LAM dataset in .xml format and formats for YOLOv8 format.
def parse_lam_XML(filename):
    
    tree = ET.parse(filename)
    root = tree.getroot()
    
    # Image height and width
    img_w = int(root.attrib['width'])
    img_h = int(root.attrib['height'])

    # Find all bounding boxes
    for child in root:
        instances = child.findall('line')
        bboxes = []
        for instance in instances:
            attributes = instance.attrib
            w = float(attributes['w'])
            h = float(attributes['h'])
            x = float(attributes['x'])
            y = float(attributes['y'])
            
            # YOLOv8 likes centered coordinates
            x_cent = x + w/2
            y_cent = y + h/2
            
            # YOLOv8 likes normalized coordinates
            x_cent_norm = x_cent/img_w
            y_cent_norm = y_cent/img_h
            w_norm = w/img_w
            h_norm = h/img_h
            
            # The random zero is because we only define one class as 'handwriting' in the .yaml file
            bboxes.append([0, x_cent_norm, y_cent_norm, w_norm, h_norm])
        return bboxes
    
# Writes bounding boxes to a .txt file in YOLOv8 format.
def bboxes_to_txt(filename, bboxes):
    f= open(filename[:-4] + '.txt',"w+")
    for bbox in bboxes:
        for i in range(len(bbox)):
            f.write(str(bbox[i]))
            if i != len(bbox):
                f.write(' ')
        f.write('\n')

# Converts entire directory to YOLOv8 format.
def convert_lam_directory(in_path, out_path):

    xml_list = Path(in_path).rglob('./xml/*.xml')
    jpg_list = Path(in_path).rglob('./img/*.jpg')

    label_path = out_path + '/labels/'
    image_path = out_path + '/images/'

    if not os.path.exists(label_path):
        os.makedirs(label_path)

    if not os.path.exists(image_path):
        os.makedirs(image_path)

    for xml_doc in xml_list:
        filename = xml_doc.name

        if not filename[0] == '.':
            bboxes = parse_lam_XML(str(xml_doc))
            bboxes_to_txt(label_path + filename, bboxes)
        
        for jpg_img in jpg_list:
            filename = jpg_img.name
            print("Move: " + in_path + '/img/' + filename + " -> " + image_path + filename)
            shutil.move(Path(in_path + '/img/' + filename),Path(image_path + filename))    
            
def parse(directory):
    dir_list = os.listdir(directory)
    for folder in dir_list:
        abs_path = str(os.path.abspath(directory)) 
        folder_path = abs_path + '/' + str(folder)
        convert_lam_directory(folder_path, abs_path)
        
# RUN SCRIPT HERE #############################################################

# Aim this at your LAM dataset /full_pages/ directory like here:
directory = 'C:/some_path_that_you_need_to_change/LAM/full_pages'
parse(directory)
