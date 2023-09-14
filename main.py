# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 07:21:39 2023

@author: Lincoln Scheer

@breif: This script is a minial reproduceable attempt at training a YOLOv8 
        model to detect handwriting instances in an image.
        
        
        Predictions Located:
            ./runs/detect/predict<RUN NUMBER>/
            
        Trained Models Located:
            ./runs/detect/train<RUN NUMBER>/
            
        Training Datasets Located:
            ./runs/datasets/
            
"""

import os
from ultralytics import YOLO
from pathlib import Path


# Code wont run on windows if this is not set. No workaround as of 9/10 -LS
os.environ["KMP_DUPLICATE_LIB_OK"] = "1"


# Using a pretrained network on object detection, might not be beneficial -LS
# Other Models: https://docs.ultralytics.com/models/yolov8/#key-features
original_yaml = 'yolov8n.yaml';
original_pt = 'yolov8n.pt'


# Using dataset annotated with 8 images, not a good training set. Un-comment
# the line below it to use a handwriting dataset I got from roboflow. -LS
# Loads
model = YOLO(original_yaml)
model = YOLO(original_pt)
model = YOLO(original_yaml).load(original_pt)


# Define and get path for training datasets
train_yaml = "C:/some_path_that_you_need_to_change/LAM/full_pages"


# Train model
#
# Epochs (Training Iterations)
# Batch (Images Before Next Gradient Descent Recalculation)
#
# I used 10 epochs and 16 batch for my runs, I want to increase epochs to get
# a better trained model hopefully.
#
results = model.train(data=str(Path(train_yaml).resolve()),
                      epochs=10,
                      batch=16,
                      verbose=True
                      )


# Define and get path for training datasets
# train_yaml = "datasets/ls-annot-8/data.yaml"

# results = model.train(data=str(Path(train_yaml).resolve()),
#                       epochs=32,
#                       batch=16,
#                       verbose=True
#                       )


# After model is trained predict on some test images
model.predict('records/', save=True)