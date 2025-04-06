'''
This Python script reads in an image selected from a file dialog window, detects circles using the 
HoughCircles function in OpenCV, an dislpays the image with the detected circles marked.
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

input_img_path = filedialog.askopenfilename(title="Select an image", 
                                            initialdir=os.getcwd(), 
                                            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("All files", "*.*")])

image = cv2.imread(input_img_path)
input_window_name = "Input Image"
cv2.imshow(input_window_name, resize_image_to_fit_screensize(image))
gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray_img_blur = cv2.medianBlur(gray_img, 5)

# circles = cv2.HoughCircles(gray_img, cv2.HOUGH_GRADIENT,
#                             dp, minDist, param1=100, param2=100,
#                             minRadius=0, maxRadius=0)
#Param 1 will set the sensitivity; how strong the edges of the circles need to 
# be. Too high and it won't detect anything, too low and it will find too much 
# clutter. Param 2 will set how many edge points it needs to find to declare 
# that it's found a circle. Again, too high will detect nothing, too low will 
# declare anything to be a circle. The ideal value of param 2 will be related to 
# the circumference of the circles.
circles = cv2.HoughCircles(gray_img_blur, cv2.HOUGH_GRADIENT, dp=1.2, minDist=100)
print("Number of circles detected is", len(circles[0,:]))

if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(image, center=(i[0], i[1]), radius=i[2], color=(0, 255, 0), thickness=5)
        # draw the center of the circle
        cv2.circle(image, center=(i[0], i[1]), radius=2, color=(0, 0, 255), thickness=3)

output_window_name = "Output Circle Detection HoughCircles"
cv2.imshow(output_window_name, resize_image_to_fit_screensize(image))
cv2.waitKey(0) # Waits indefinitely for a key press before proceeding
cv2.destroyAllWindows()