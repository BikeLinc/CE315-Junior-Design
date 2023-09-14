import os
from pathlib import Path
import numpy as np
import shutil
import random

# RUN SCRIPT HERE #############################################################

directory = 'C:/some_path_that_you_need_to_change/LAM/full_pages'

# This defines how much data we set aside for validation the rest is for training. (0-1 scalar)
valid_size = 0.3

# Rest Of Scrpt ###############################################################

# Write YAML datafile
print(directory + '/data.yaml')
yaml_file = open(Path(directory + '/data.yaml'),"w+")
yaml_file.write(str("train: ./train/images\n"))
yaml_file.write(str("val: ./valid/images\n"))
yaml_file.write(str("test: ./test/images\n"))
yaml_file.write(str('\n'))
yaml_file.write(str("nc: 1\n"))
yaml_file.write(str("names: ['Handwriting']\n"))
yaml_file.close()

# Create Directories
img_dir = directory + '/images'
lbl_dir = directory + '/labels'
train_dir = directory + '/train'
valid_dir = directory + '/valid'
jpg_list = Path(img_dir).rglob('./*.jpg')
txt_list = Path(lbl_dir).rglob('./*.txt')

jpgs = []
txts = []
for jpg in jpg_list:
    jpgs.append(jpg)

for txt in txt_list:
    txts.append(txt)

random.shuffle(jpgs)
size = len(jpgs)

valid_split_size = int(np.floor(size*valid_size))
train_split_size = size - valid_split_size
valid_split_jpg = jpgs[0:valid_split_size]
valid_split_txt = txts[0:valid_split_size]
train_split_jpg = jpgs[valid_split_size:size]
train_split_txt = txts[valid_split_size:size]

if not os.path.exists(train_dir + '/images'):
        os.makedirs(train_dir + '/images')

if not os.path.exists(valid_dir + '/images'):
        os.makedirs(valid_dir + '/images')

if not os.path.exists(train_dir + '/labels'):
        os.makedirs(train_dir + '/labels')

if not os.path.exists(valid_dir + '/labels'):
        os.makedirs(valid_dir + '/labels')

for img in train_split_jpg:
    print('Copy: ' + str(img) + " -> " + train_dir + '/images/' + img.name)
    shutil.copy(str(img), train_dir + '/images/' + img.name) 

for txt in train_split_txt:
    print('Copy: ' + str(txt) + " -> " + train_dir + '/labels/' + txt.name)
    shutil.copy(str(txt), train_dir + '/labels/' + txt.name) 

for img in valid_split_jpg:
    print('Copy: ' + str(img) + " -> " + valid_dir + '/images/' + img.name)
    shutil.copy(str(img), valid_dir + '/images/' + img.name) 

for txt in valid_split_txt:
    print('Copy: ' + str(txt) + " -> " + valid_dir + '/labels/' + txt.name)
    shutil.copy(str(txt), valid_dir + '/labels/' + txt.name) 