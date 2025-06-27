# model.py
import os, cv2
import numpy as np
import pandas as pd
import seaborn as sns
from flask import Flask, request, render_template, send_from_directory
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Flatten, Dense
from tensorflow.keras.applications import MobileNetV3Small
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.applications.inception_v3 import preprocess_input
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping
import matplotlib.pyplot as plt

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def get_data(data_dir, img_size=224):
    img_data, labels = [], []
    class_names = os.listdir(data_dir)
    for label in class_names:
        path = os.path.join(data_dir, label)
        class_num = class_names.index(label)
        for img in os.listdir(path):
            try:
                img_arr = cv2.imread(os.path.join(path, img), cv2.IMREAD_COLOR)
                resized_arr = cv2.resize(img_arr, (img_size, img_size))
                img_data.append(resized_arr)
                labels.append(class_num)
            except Exception as e:
                print(e)
    return np.array(img_data), to_categorical(np.array(labels)), class_names

# Place training logic inside a function if needed
