import tensorflow as tf
from internal.params import params
import cv2
import numpy as np

class Model:
    def __init__(self, class_names):
        self.class_names = class_names

    def detect(self, frame):
        raise NotImplementedError("cannot use an instance of abstract class Model")

class TFModel(Model):
    def __init__(self, class_names):
        super().__init__(class_names)

        self.input_size = params.TF.INPUT_SIZE
        self.model = tf.saved_model.load(str(params.TF.SAVED_MODEL_PATH))
        self.infer = self.model.signatures['serving_default']

    def detect(self, frame):
        frame = np.asarray(frame)
        image_h, image_w = frame.shape[:2]

        image_data = cv2.resize(frame, (self.input_size, self.input_size))
        input_tensor = tf.convert_to_tensor(image_data)
        input_tensor = input_tensor[tf.newaxis,...]

        pred = self.infer(input_tensor)

        boxes = pred['detection_boxes'].numpy()
        scores = pred['detection_scores'].numpy()
        classes = pred['detection_classes'].numpy()
        valid_detections = int(pred['num_detections'])

        # initialize empty list to be passed
        cl = []
        bbox = []
        confs = []

        for i in range(valid_detections):
            # shouldn't be necessary, just for safety measures
            if int(classes[0][i]) < 0 or int(classes[0][i]) > len(self.class_names):
                continue

            coor = boxes[0][i].copy()

            # get bounding boxes
            coor[0] = int(coor[0] * image_h)  # y1
            coor[1] = int(coor[1] * image_w)  # x1
            coor[2] = int(coor[2] * image_h)  # y2
            coor[3] = int(coor[3] * image_w)  # x2

            class_ind = int(classes[0][i])

            cl.append(class_ind)
            bbox.append([coor[1], coor[0], coor[3], coor[2]])
            confs.append(scores[0][i])

        return bbox, confs, cl
