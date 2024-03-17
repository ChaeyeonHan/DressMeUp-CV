# -*- coding: utf-8 -*-
"""clothremovebackground.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xfIyyK051qGt2QJDdIl0oOlouH4u2oFf
"""

# # 실행해주어야함
# !pip install rembg

import cv2
import numpy as np
from matplotlib import pyplot as plt
from rembg import remove
from PIL import Image


# # 이미지 경로
# cloth_path = "/content/drive/MyDrive/dressmeup/cloth-segmentation/input/반바지1.jpg"
# cloth_parsing_path = "/content/drive/MyDrive/dressmeup/cloth-segmentation/output/cloth_seg/final_seg1.png"


# result="bottom"

#
def process_cloth_image(cloth_parsing_path, cloth_path, result):

  if result=="top":
    clothparsing = cv2.imread(cloth_parsing_path)
    clothparsing_hsv = cv2.cvtColor(clothparsing, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 40, 40])
    upper_red = np.array([10, 255, 255])
    mask_red1 = cv2.inRange(clothparsing_hsv, lower_red, upper_red)
    lower_red = np.array([170, 40, 40])
    upper_red = np.array([180, 255, 255])
    mask_red2 = cv2.inRange(clothparsing_hsv, lower_red, upper_red)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours_red:
      contour = max(contours_red, key=cv2.contourArea)
      cloth_image = cv2.imread(cloth_path)
      result_image = np.zeros_like(cloth_image)
      cv2.drawContours(result_image, [contour], 0, (255, 255, 255), thickness=cv2.FILLED)
      result_image = cv2.bitwise_and(cloth_image, result_image)



  elif result=="bottom":
    clothparsing = cv2.imread(cloth_parsing_path)
    clothparsing_hsv = cv2.cvtColor(clothparsing, cv2.COLOR_BGR2HSV)
    lower_green = np.array([30, 40, 40])
    upper_green = np.array([90, 255, 255])
    mask_green= cv2.inRange(clothparsing_hsv, lower_green, upper_green)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours_green:
      contour = max(contours_green, key=cv2.contourArea)
      cloth_image = cv2.imread(cloth_path)
      result_image = np.zeros_like(cloth_image)
      cv2.drawContours(result_image, [contour], 0, (255, 255, 255), thickness=cv2.FILLED)
      result_image = cv2.bitwise_and(cloth_image, result_image)



  else:
    clothparsing = cv2.imread(cloth_parsing_path)
    clothparsing_hsv = cv2.cvtColor(clothparsing, cv2.COLOR_BGR2HSV)
    lower_green = np.array([30, 40, 40])
    upper_green = np.array([90, 255, 255])
    mask_green= cv2.inRange(clothparsing_hsv, lower_green, upper_green)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours_green:
      contour = max(contours_green, key=cv2.contourArea)
      cloth_image = cv2.imread(cloth_path)
      result_image = np.zeros_like(cloth_image)
      cv2.drawContours(result_image, [contour], 0, (255, 255, 255), thickness=cv2.FILLED)
      result_image = cv2.bitwise_and(cloth_image, result_image)

  output=remove(result_image)
  gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
  _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
  contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  max_contour = max(contours, key=cv2.contourArea)
  x, y, w, h = cv2.boundingRect(max_contour)
  cropped_image = output[y:y+h, x:x+w]


  return cropped_image



# result_image=process_cloth_image(cloth_parsing_path, cloth_path, result)
# output_path = "/content/drive/MyDrive/dressmeup/cloth-segmentation/output/cloth_final1.png"
# cv2.imwrite(output_path, result_image)
# cv2_imshow(result_image)





