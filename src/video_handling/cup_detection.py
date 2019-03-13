import cv2
import imutils as imt
import os
import glob
import math
import numpy as np

"""
To understand how it works see the ocv_threshhold.ipynb ipython notebook
"""


def prehandling(bgr, clipLimit=20.0, tileGridSize=(6,6)):
    clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=tileGridSize)
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
    lab_planes = cv2.split(lab)
    lab_planes[0] = clahe.apply(lab_planes[0])
    lab = cv2.merge(lab_planes)
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

def thresh_holding(rgb, color, weight):
    img = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    thresh_lambda = lambda ind: cv2.bitwise_and(\
                cv2.threshold(img[:,:,ind],\
                color[ind]-weight[ind],255,\
                cv2.THRESH_BINARY)[1],\
                cv2.threshold(img[:,:,ind],\
                color[ind]+weight[ind],255,\
                cv2.THRESH_BINARY_INV)[1],\
                )

    thrs = [thresh_lambda(i) for i in range(3)]
    rgthr = cv2.bitwise_and(thrs[0], thrs[1])
    bthr = cv2.bitwise_and(thrs[2], rgthr)
    return bthr

def overlap(rect1, rect2):
    """
    calculate area overlap
    rect is two point left top and bottom right
    """
    delta_x = min(rect2[1][0], rect1[1][0]) - max(rect2[0][0], rect1[0][0])
    delta_y = min(rect2[1][1], rect1[1][1]) - max(rect2[0][1], rect1[0][1])
    common = delta_x * delta_y if delta_x > 0 and delta_y > 0 else 0
    area1 = abs(rect1[0][0] - rect1[1][0]) * abs(rect1[0][1] - rect1[1][1])
    area2 = abs(rect2[0][0] - rect2[1][0]) * abs(rect2[0][1] - rect2[1][1])
    return 2 * common / (area1 + area2)


def windows_fill_calc(color_mask_matrix,  window_size=250, threshhold=0.5, overlap_threshhold=0.75):
    
    template = np.full((window_size, window_size), 255, dtype=color_mask_matrix.dtype)
    
    matchResult = cv2.matchTemplate(color_mask_matrix, template, cv2.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(matchResult)
    
    #handmade normalization
    res = matchResult /  max_val
    
    #plt.imshow(res, cmap="gray")
    results = []
    min_val, max_val, min_loc, max_loc = 0, 1, 0, 0
    while max_val > threshhold:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val > threshhold:
            bottom_right = (max_loc[0]+window_size, max_loc[1]+window_size)
            results.append((max_loc, bottom_right))
            
            #to avoid finding this place the next time
            res[max_loc[1]:bottom_right[1], max_loc[0]:bottom_right[0]] = 0
    
    
    #union rectangles with a big overlap area
    i = 0
    while i < len(results):
        detect = results[i]
        
        j = 0
        while j < len(results):
            if j != i and overlap(detect, results[j]) > overlap_threshhold:
                #union two rect
                xl, xr = min(detect[0][0], results[j][0][0]), max(detect[1][0], results[j][1][0])
                yl, yr = min(detect[0][1], results[j][0][1]), max(detect[1][1], results[j][1][1])
                results[i] = ((xl, yl), (xr, yr))
                detect = results[i]
                
                
                results.remove(results[j])
                
                if j < i:
                    i -= 1
            j += 1
        
        i += 1
                
                
    
    return results

def draw_detections(img, detections):
    COLOR = (0, 0, 255)
    for detected in detections:
        cv2.rectangle(img, detected[0],  detected[1], COLOR, 3)

class SimpleHSVDetector:
    
    def __init__(self, color=(125,70,70), weight_color=(20,40,40),  window_size=250, 
                 threshhold=0.98, overlap_threshhold=0.75,
                 clipLimit=5.0, tileGridSize=(6,6)):
        """
        color should in HSV
        """
        self.color, self.weight_color, self.window_size = color, weight_color, window_size
        self.threshhold, self.overlap_threshhold = threshhold, overlap_threshhold
        self.clipLimit, self.tileGridSize = clipLimit, tileGridSize
        
    def detect(self, bgr):
        bgr = prehandling(bgr, clipLimit=self.clipLimit, tileGridSize=self.tileGridSize)
        rgb = cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB)
        gray_scale = thresh_holding(rgb, self.color, self.weight_color)
        
        return windows_fill_calc(gray_scale, threshhold=self.threshhold, window_size=self.window_size, overlap_threshhold=self.overlap_threshhold)
