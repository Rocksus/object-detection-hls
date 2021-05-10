import cv2
import colorsys
import random
import numpy as np
from internal.params import params

# Constants
ALPHA = params.VIZ.ALPHA
FONT = params.VIZ.FONT
TEXT_SCALE = params.VIZ.TEXT_SCALE
TEXT_THICKNESS = params.VIZ.TEXT_THICKNESS

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def gen_colors(num_colors):
    hsvs = [[float(x) / num_colors, 1.0, 0.7] for x in range(num_colors)]
    random.seed(1234)
    random.shuffle(hsvs)
    rgbs = list(map(lambda x: list(colorsys.hsv_to_rgb(*x)), hsvs))
    bgrs = [(int(rgb[2] * 255), int(rgb[1] * 255), int(rgb[0] * 255)) for rgb in rgbs]
    return bgrs


def draw_boxed_text(img, text, topleft, color):
    assert img.dtype == np.uint8
    img_h, img_w, _ = img.shape
    if topleft[0] >= img_w or topleft[1] >= img_h:
        return img
    margin = 3
    size = cv2.getTextSize(text, FONT, TEXT_SCALE, TEXT_THICKNESS)
    w = size[0][0] + margin * 2
    h = size[0][1] + margin * 2
    # the patch is used to draw boxed text
    patch = np.zeros((h, w, 3), dtype=np.uint8)
    patch[...] = color
    cv2.putText(
        patch,
        text,
        (margin + 1, h - margin - 2),
        FONT,
        TEXT_SCALE,
        WHITE,
        thickness=TEXT_THICKNESS,
        lineType=cv2.LINE_8,
    )
    cv2.rectangle(patch, (0, 0), (w - 1, h - 1), BLACK, thickness=1)
    w = min(w, img_w - topleft[0])  # clip overlay at image boundary
    h = min(h, img_h - topleft[1])
    
    # Overlay the boxed text onto region of interest (roi) in img
    roi = img[topleft[1] : topleft[1] + h, topleft[0] : topleft[0] + w, :]
    cv2.addWeighted(patch[0:h, 0:w, :], ALPHA, roi, 1 - ALPHA, 0, roi)
    return img

class Visualizer:
    def __init__(self, cls_dict):
        self.cls_dict = cls_dict
        self.colors = gen_colors(len(cls_dict))

    def draw_bboxes(self, img, boxes, confs, clss):
        for bb, cf, cl in zip(boxes, confs, clss):
            cl = int(cl)
            x_min, y_min, x_max, y_max = bb[0], bb[1], bb[2], bb[3]
            color = self.colors[cl]
            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color, 2)
            txt_loc = (int(max(x_min + 2, 0)), int(max(y_min + 2, 0)))
            cls_name = self.cls_dict[cl]
            txt = "{} {:.2f}".format(cls_name, cf)
            img = draw_boxed_text(img, txt, txt_loc, color)
        return img
