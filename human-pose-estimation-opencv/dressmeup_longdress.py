# -*- coding: utf-8 -*-
"""dressmeup_longdress.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nbooXki28tVBfc7fe3tf2OHNOSHGj98_
"""

import cv2
import numpy as np
# from google.colab.patches import cv2_imshow


# image_path ="/content/drive/MyDrive/dressmeup/human-pose-estimation-opencv/달리남자2.webp"
# cloth_path = "/content/drive/MyDrive/dressmeup/cloth-segmentation/output/cloth_final.png"


def longdress(image_path, cloth_path):
    # 이미지와 옷 불러오기
    image = cv2.imread(image_path)
    cloth = cv2.imread(cloth_path)

    # POSE_PAIRS와 BODY_PARTS 정의
    BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
               "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
               "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
               "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

    POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
               ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
               ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
               ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
               ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]

    width = 368
    height = 368
    inWidth = width
    inHeight = height


    net = cv2.dnn.readNetFromTensorflow("graph_opt.pb")
    thr = 0.2

    def poseDetector(frame):
        processed_frame = frame.copy()

        frameWidth = frame.shape[1]
        frameHeight = frame.shape[0]

        net.setInput(cv2.dnn.blobFromImage(frame, 1.0, (inWidth, inHeight), (127.5, 127.5, 127.5), swapRB=True, crop=False))
        out = net.forward()
        out = out[:, :19, :, :]
        assert(len(BODY_PARTS) == out.shape[1])

        points = []
        for i in range(len(BODY_PARTS)):
            heatMap = out[0, i, :, :]

            _, conf, _, point = cv2.minMaxLoc(heatMap)
            x = (frameWidth * point[0]) / out.shape[3]
            y = (frameHeight * point[1]) / out.shape[2]
            points.append((int(x), int(y)) if conf > thr else None)

        for pair in POSE_PAIRS:
            partFrom = pair[0]
            partTo = pair[1]
            assert(partFrom in BODY_PARTS)
            assert(partTo in BODY_PARTS)

            idFrom = BODY_PARTS[partFrom]
            idTo = BODY_PARTS[partTo]

            if points[idFrom] and points[idTo]:
                cv2.line(processed_frame, points[idFrom], points[idTo], (0, 255, 0), 3)
                cv2.ellipse(processed_frame, points[idFrom], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)
                cv2.ellipse(processed_frame, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)

        t, _ = net.getPerfProfile()
        LShoulder = points[BODY_PARTS["LShoulder"]]
        RShoulder = points[BODY_PARTS["RShoulder"]]
        RAnkle = points[BODY_PARTS["RAnkle"]]
        LAnkle= points[BODY_PARTS["LAnkle"]]

        return LShoulder, RShoulder, RAnkle, LAnkle, frame

    # poseDetector 함수를 사용하여 이미지 처리
    LShoulder, RShoulder, RAnkle, LAnkle, image = poseDetector(image)


    # x 값 차이 계산
    x_diffshoulder = (RShoulder[0] - LShoulder[0]) * 0.5
    x_diffancle= (RAnkle[0] -LAnkle[0]) * 0.7

    # y 값 차이 계산
    y_left = (LShoulder[1] - LAnkle[1]) * 0.07
    y_right = (RShoulder[1] - RAnkle[1]) * 0.07


    # y값 차이 계산
    # LShoulder1, RShoulder1, RWrist1, LWrist1 좌표 수정
    LShoulder1 = (LShoulder[0] - int(x_diffshoulder), LShoulder[1] + int(y_left))
    RShoulder1 = (RShoulder[0] + int(x_diffshoulder), RShoulder[1] + int(y_right))
    LAnkle1 = (LAnkle[0] - int(x_diffancle), LAnkle[1]+ int(y_left) )
    RAnkle1 = (RAnkle[0] + int(x_diffancle), RAnkle[1]+ int(y_right) )

    # 변환 행렬 계산
    pts_src = np.float32([[0, 0], [cloth.shape[1], 0], [cloth.shape[1], cloth.shape[0]], [0, cloth.shape[0]]])
    pts_dst = np.float32([LShoulder1, RShoulder1, RAnkle1, LAnkle1])
    matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)
    # 옷 이미지를 메인 이미지에 변환하여 오버레이
    cloth_warped = cv2.warpPerspective(cloth, matrix, (image.shape[1], image.shape[0]))

    # 메인 이미지 위에 옷 이미지를 올바르게 적용
    result = image.copy()
    for y in range(cloth_warped.shape[0]):
        for x in range(cloth_warped.shape[1]):
            if np.all(cloth_warped[y, x] != [0, 0, 0]):
                result[y, x] = cloth_warped[y, x]

    return result

# result_image = longdress(image_path, cloth_path)