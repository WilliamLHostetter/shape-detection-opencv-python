'''
This script reads in an image selected from a file dialog window, detects lines 
(segments) using the probiblistic Hough transform (HoughLinesP), an dislpays the 
image with the detected lines marked.
'''

import os
from tkinter import filedialog
import cv2 # OpenCV Library
import numpy as np
import ctypes # to get screen size


def resize_image_to_fit_screensize(img):
    ## get Screen Size
    user32 = ctypes.windll.user32
    (screensize_width, screensize_height) = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1) 
    # print("(screensize_width, screensize_height) =", (screensize_width, screensize_height))
    img_resized = img
    max_width = int(0.6*screensize_width)
    max_height = int(0.6*screensize_height)
    (img_height, img_width) = img.shape[:2]
    img_aspect_ratio = float(img_width)/float(img_height)
    if img_width <= max_width and img_height <= max_height:
        return img
    output_width = img_width
    output_height = img_height
    if output_width > max_width:
        output_width = max_width
        output_height = int(float(output_width)/img_aspect_ratio)
    if output_height > max_height:
        output_height = max_height
        output_width = int(float(output_height)*img_aspect_ratio)
    # print("(output_width, output_height) =", (output_width, output_height))
    img_resized = cv2.resize(img, (output_width, output_height))
    return img_resized

input_img_path = filedialog.askopenfilename(title="Select an image", initialdir=os.getcwd(), filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("All files", "*.*")])

img = cv2.imread(input_img_path)
input_window_name = "Input Image"
cv2.imshow(input_window_name, resize_image_to_fit_screensize(img))
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray_img, 50, 120)
lines = cv2.HoughLinesP(edges, rho=1,
                        theta=np.pi/180.0,
                        threshold=20,
                        minLineLength=40,
                        maxLineGap=5)
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.imshow("Output Line Edges", resize_image_to_fit_screensize(edges))
cv2.imshow("Output Line Detections", resize_image_to_fit_screensize(img))
cv2.waitKey(0) # Waits indefinitely for a key press before proceeding
cv2.destroyAllWindows()
