"""
params.py will contain all of the parameters required by the model
"""
from easydict import EasyDict as edict
import cv2
from os import path

__C = edict()

params = __C

__C.URL = "http://localhost:8000/streams/output.m3u8"
__C.CLASS_NAMES_PATH = path.join(
    path.dirname(__file__), "..", "models", "labels.txt"
)

__C.VIZ = edict()

__C.VIZ.ALPHA = 0.5
__C.VIZ.FONT = cv2.FONT_HERSHEY_PLAIN
__C.VIZ.TEXT_SCALE = 1.0
__C.VIZ.TEXT_THICKNESS = 1

__C.TF = edict()

__C.TF.INPUT_SIZE = 300
__C.TF.SAVED_MODEL_PATH = path.join(
    path.dirname(__file__), "..", "models", "ssd_mobilenet_v1_coco_2018_01_28", "saved_model"
)