'''
Identifies shapes (Triangle, Quadrilateral, Pentagon, Star, or Circle) in an 
input image using contours and labels each shape in the output image.
Triangle = a three-sided polygon with three corners and three sides
Quadrilateral = a four-sided polygon, having four edges (sides) and four corners (vertices)
Pentagon = a five-sided polygon, having five edges (sides) and five corners (vertices)
Hexagon = a six-sided polygon, having six edges (sides) and six corners (vertices)
Circle = the set of all points in a plane that are equidistant from a given point, known as the center.
'''

from tkinter import filedialog
import cv2 # OpenCV Library
import os # to get current working directory os.getcwd()
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

# Input image to detect shapes on
input_img_path = filedialog.askopenfilename(title="Select an image", initialdir=os.getcwd(), filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"),  ("All files", "*.*")])
print("input_img_path =", input_img_path)
image = cv2.imread(input_img_path)
input_window_name = "Input Image"
cv2.imshow(input_window_name, resize_image_to_fit_screensize(image))

# Converting to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

# Blurring image can help reduce noise and fine details that might interfere with the shape detection process. 
gray_image_blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)
# cv2.imshow("gray_image_blurred", resize_image_to_fit_screensize(gray_image_blurred))
median_value = np.median(gray_image_blurred)
# print("median level of input image =", median_value)
gray_image_blurred_bkg_sub = cv2.absdiff(gray_image_blurred, median_value)
# cv2.imshow("gray_image_blurred_bkg_sub", resize_image_to_fit_screensize(gray_image_blurred_bkg_sub))

# Binary threshold grayscale image (this checks every pixel, and depending on how
# bright the pixel is, the threshold value will convert the pixel to either black or white (0 or 1)).
# cv2.threshold(src, thresholdValue, maxValue, threshold type)
# src: The source image, which should be grayscale.
# thresholdValue: The threshold value used to classify the pixel values.
# maxValue: The maximum value that can be assigned to a pixel.
# threshold type: The method of thresholding to be applied, such as cv2.THRESH_BINARY, cv2.THRESH_BINARY_INV, cv2.THRESH_TRUNC, cv2.THRESH_TOZERO, or cv2.THRESH_TOZERO_INV.
# _, thresh_image = cv2.threshold(gray_image_blurred, 220, 255, cv2.THRESH_BINARY)
_, thresh_image = cv2.threshold(gray_image_blurred_bkg_sub, 10, 255, cv2.THRESH_BINARY)
# cv2.imshow("Threshold Image", resize_image_to_fit_screensize(thresh_image))

# Retrieving outer-edge coordinates in the new threshold image
# cv2.findContours(source image, contour retrieval mode, contour approximation method) 
# cv2.RETR_TREE retrieves all of the contours and reconstructs a full hierarchy of nested contours
# The contour approximation method specifies how the contours are compressed. 
# cv2.CHAIN_APPROX_NONE stores all the boundary points, whereas 
# cv2.CHAIN_APPROX_SIMPLE compresses the contour by removing all redundant points, storing only the start and end points of each line segment.
contours, hierarchy = cv2.findContours(thresh_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
# contours, hierarchy = cv2.findContours(thresh_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Iterating through each contour to retrieve coordinates of each shape
for i, contour in enumerate(contours):
    # print("i =", i)
    # approximate the contour
    epsilon = 0.01*cv2.arcLength(contour, True) # returns epsilon value to specify the precision in approximating our shape
    # approxPolyDP(input_curve, epsilon, closed)
    # curve: The array of contour points.
    # epsilon: The maximum distance from the contour to the approximated contour. A wise selection of epsilon is needed to get the correct output.
    # closed: A boolean value indicating whether the approximated curve is closed (True) or not (False).
    # approx = cv2.approxPolyDP(curve=contour, epsilon=epsilon, closed=True) # returns a resampled contour, a set of (x, y) points that form the approximated polygonal curve.
    approx = cv2.approxPolyDP(contour, epsilon, True)
    # print("epsilon =", epsilon)
    # print("len(approx) =", len(approx))

    # Drawing the outer-edges onto the image
    # cv.drawContours(image, contours, contourIdx, color[, thickness[, lineType[, hierarchy[, maxLevel[, offset]]]]]) -> 	image
    cv2.drawContours(image, contour, -1, (0, 255, 0), 4)

    # Retrieving coordinates of the contour so that we can put text over the shape.
    x, y, w, h = cv2.boundingRect(approx)
    x_mid = int(x + (w/3)) # This is an estimation of where the middle of the shape is in terms of the x-axis.
    y_mid = int(y + (h/1.5)) # This is an estimation of where the middle of the shape is in terms of the y-axis.

    # Setting some variables which will be used to display text on the final image
    # cv.putText(img, text, org, fontFace, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]]) -> img
    text_coordinates = (x_mid, y_mid)
    fontScale = 1
    if median_value > 255/2:
        text_color = (0, 0, 0) # black
    else:
        text_color = (255, 255, 255) # white
    text_font = cv2.FONT_HERSHEY_DUPLEX
    text_thickness = 1  

    # Identify the shape by the number of edges the contour has. 
    if len(approx) == 3:
        cv2.putText(image, "Triangle", text_coordinates, text_font, text_thickness, text_color, text_thickness) # Text on the image
    elif len(approx) == 4: # square / rectangle / parallelogram /
        cv2.putText(image, "Quadrilateral", text_coordinates, text_font, text_thickness, text_color, text_thickness)
    elif len(approx) == 5: 
        cv2.putText(image, "Pentagon", text_coordinates, text_font, fontScale, text_color, text_thickness)
    elif len(approx) == 6:
        cv2.putText(image, "Hexagon", text_coordinates, text_font, fontScale, text_color, text_thickness)
    elif len(approx) == 10:
        cv2.putText(image, "Star", text_coordinates, text_font, fontScale, text_color, text_thickness)
    else:
        # If the length is not any of the above, we assume the shape/contour to be a circle.
        cv2.putText(image, "Circle", text_coordinates, text_font, fontScale, text_color, text_thickness)
    
# Displaying the image with the detected shapes onto the screen
output_window_name = "Output"
cv2.imshow(output_window_name, resize_image_to_fit_screensize(image))
cv2.waitKey(0) # Waits indefinitely for a key press before proceeding
cv2.destroyAllWindows()
