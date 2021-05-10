import logging
import sys

import cv2
import numpy as np

import internal.utils as utils
from internal.model import TFModel
from internal.params import params
from internal.visualizer import Visualizer


class Detector:
    def __init__(self, input_url):
        self._logger = logging.getLogger(__package__)
        self.url = input_url
        self.class_names = utils.read_class_names(params.CLASS_NAMES_PATH)
        self.model = TFModel(self.class_names)
        self._running = True
        self.viz = Visualizer(self.class_names)
    
    def run(self):
        cap = cv2.VideoCapture(self.url)
        if cap.isOpened() == False:
            print(f"unable to open url '{self.url}'")
            sys.exit(-1)

        fps = cap.get(cv2.CAP_PROP_FPS)
        wait_ms = int(1000 / fps)

        while self._running:
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                print("video stream ended")
                break
        
            boxes, confidences, classes = self.model.detect(frame)

            result = np.asarray(frame)
            result = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
            result = self.viz.draw_bboxes(result, boxes, confidences, classes)

            cv2.imshow("Detection", result)
            if cv2.waitKey(wait_ms) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

    def terminate(self):
        self._running = False
