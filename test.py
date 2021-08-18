# coding=utf-8
import numpy as np
from PIL import Image
import cv2


# import dlib


def ellipse_detect(image):
    """YCrCb椭圆肤色模型进行肤色检测"""
    img = cv2.imread(image, cv2.IMREAD_COLOR)
    skinCrCbHist = np.zeros((256, 256), dtype=np.uint8)
    cv2.ellipse(skinCrCbHist, (113, 155), (23, 15), 43, 0, 360, (255, 255, 255), -1)
    YCRCB = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    (y, cr, cb) = cv2.split(YCRCB)
    skin = np.zeros(cr.shape, dtype=np.uint8)
    (x, y) = cr.shape
    for i in range(0, x):
        for j in range(0, y):
            CR = YCRCB[i, j, 1]
            CB = YCRCB[i, j, 2]
            if skinCrCbHist[CR, CB] > 0:
                skin[i, j] = 255
    nx_min = 0
    ny_min = int(0.48 * img.shape[0])
    nx_max = img.shape[1]
    ny_max = int(0.68 * img.shape[0])
    print(nx_min, ny_min, nx_max, ny_max)
    n = 0
    for i in range(ny_min, ny_max):
        for j in range(nx_min, nx_max):
            # print(skin[i][j])
            if skin[i][j] == 0:
                n = n + 1
    nose_masked = n * 1.0 / ((nx_max - nx_min) * (ny_max - ny_min))
    print(nose_masked)
    if nose_masked >= 0.7:
        a = 1
    else:
        a = 0
    mx_min = 0
    my_min = ny_max
    mx_max = img.shape[1]
    my_max = int(0.95 * img.shape[0])
    print(mx_min, my_min, mx_max, my_max)
    # cropped_ = img_.crop((mx_min, my_min, mx_max, my_max))
    # cropped_.show()
    m = 0
    for i in range(my_min, my_max):
        for j in range(mx_min, mx_max):
            # print(skin[i][j])
            if skin[i][j] == 0:
                m = m + 1
    mouth_masked = m * 1.0 / ((mx_max - mx_min) * (my_max - my_min))
    print(mouth_masked)
    if mouth_masked >= 0.75:
        b = 1
    else:
        b = 0
    if a == 0 or b == 0:
        return 0
    else:
        return 1


def cr_otsu(image):
    """YCrCb颜色空间的Cr分量+Otsu阈值分割"""
    img = cv2.imread(image, cv2.IMREAD_COLOR)
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)

    (y, cr, cb) = cv2.split(ycrcb)
    cr1 = cv2.GaussianBlur(cr, (5, 5), 0)
    _, skin = cv2.threshold(cr1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    nx_min = 0
    ny_min = int(0.48 * img.shape[0])
    nx_max = img.shape[1]
    ny_max = int(0.68 * img.shape[0])
    print(nx_min,ny_min,nx_max,ny_max)
    img_ = Image.open(image)
    cropped = img_.crop((nx_min,ny_min,nx_max,ny_max))
    cropped.show()
    n = 0
    for i in range(ny_min, ny_max):
        for j in range(nx_min, nx_max):
            if skin[i][j] == 0:
                n = n + 1
    nose_masked = n * 1.0 / ((nx_max - nx_min) * (ny_max - ny_min))
    print(nose_masked)
    if nose_masked >= 0.65:
        a = 1
    else:
        a = 0
    mx_min = 0
    my_min = ny_max
    mx_max = img.shape[1]
    my_max = int(0.95 * img.shape[0])
    print(mx_min, my_min, mx_max, my_max)
    cropped_ = img_.crop((mx_min, my_min, mx_max, my_max))
    cropped_.show()
    m = 0
    for i in range(my_min, my_max):
        for j in range(mx_min, mx_max):
            # print(skin[i][j])
            if skin[i][j] == 0:
                m = m + 1
    mouth_masked = m * 1.0 / ((mx_max - mx_min) * (my_max - my_min))
    if mouth_masked >=0.75:
        b = 1
    else:
        b = 0
    if a == 0 or b == 0:
        return 0
    else:
        return 1


    # if(ex_max1<ex_min2):
    #     nx_min = ex_max1
    #     nx_max = ex_min2
    # else:
    #     nx_min = ex_max2
    #     nx_max = ex_min1
    # if(ey_max1>ey_max2):
    #     ny_min = int(ey_max1-0.3*(ey_max1-ey_min1))
    # else:
    #     ny_min = int(ey_max2-0.3*(ey_max2-ey_min2))
    # ny_max = int(ny_min+1.3*(ey_max1-ey_min1))
    # n=0
    # for i in range(ny_min,ny_max):
    #     for j in range(nx_min,nx_max):
    #         if(skin[i][j]==0):
    #             n = n+1
    # nose_masked = n*1.0/((nx_max-nx_min)*(ny_max-ny_min))
    # if(nose_masked>=0.7):
    #     print('1')
    # else:
    #     print('0')
    # print(skin.shape)
    # print(skin)
    #
    # dst = cv2.bitwise_and(img, img, mask=skin)
    # cv2.namedWindow("seperate", cv2.WINDOW_NORMAL)
    # cv2.imshow("seperate", dst)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


def normal_detect(img, top, left, bottom, right):
    cropped = img.crop((left, top, right, bottom))
    cropped.save("crop/20.jpg")
    path = 'crop/20.jpg'
    m = ellipse_detect(path)
    return m

    # eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    # eye_cascade.load('F:/mask_normal/MaskDetecterSystem/MaskDetecterSystem/data/haarcascades/haarcascade_eye.xml')

    # path = "29.jpg"
    # img = cv2.imread(path)
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # eyes = eye_cascade.detectMultiScale(gray, 1.2, 3)
    # i = 1
    # for (ex, ey, ew, eh) in eyes:
    #     cv2.rectangle(img, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
    #     if (i == 1):
    #         ex_min1 = ex
    #         ey_min1 = ey
    #         ex_max1 = ex + ew
    #         ey_max1 = ey + eh
    #         i = i + 1
    #     elif (i == 2):
    #         ex_min2 = ex
    #         ey_min2 = ey
    #         ex_max2 = ex + ew
    #         ey_max2 = ey + eh
    # cv2.imshow('img', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # print(ex_min1, ey_min1, ex_max1, ey_max1, ex_min2, ey_min2, ex_max2, ey_max2)
    # cr_otsu(path, ex_min1, ey_min1, ex_max1, ey_max1, ex_min2, ey_min2, ex_max2, ey_max2)

# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# # 人脸分类器
# detector = dlib.get_frontal_face_detector()
# # 获取人脸检测器
# predictor = dlib.shape_predictor(
#     "shape_predictor_68_face_landmarks.dat"
# )
#
# dets = detector(gray, 1)
# for face in dets:
#     shape = predictor(img, face)  # 寻找人脸的68个标定点
#     # 遍历所有点，打印出其坐标，并圈出来
#     for pt in shape.parts():
#         pt_pos = (pt.x, pt.y)
#         cv2.circle(img, pt_pos, 2, (0, 255, 0), 1)
#     cv2.imshow("image", img)
#
# img = Image.open("1.jpg")
# normal_detect(img,100,100,200,200)


# from PIL import Image
# import cv2
# # import dlib
#
# def cr_otsu(image):
#     """YCrCb颜色空间的Cr分量+Otsu阈值分割"""
#     img = cv2.imread(image, cv2.IMREAD_COLOR)
#     ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
#
#     (y, cr, cb) = cv2.split(ycrcb)
#     cr1 = cv2.GaussianBlur(cr, (5, 5), 0)
#     _, skin = cv2.threshold(cr1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#
#     cv2.namedWindow("image raw", cv2.WINDOW_NORMAL)
#     cv2.imshow("image raw", img)
#     cv2.namedWindow("image CR", cv2.WINDOW_NORMAL)
#     cv2.imshow("image CR", cr1)
#     cv2.namedWindow("Skin Cr+OTSU", cv2.WINDOW_NORMAL)
#     cv2.imshow("Skin Cr+OTSU", skin)
#     nx_min = 0
#     ny_min = int(0.48*img.shape[0])
#     nx_max = img.shape[1]
#     ny_max = int(0.68*img.shape[0])
#     print(nx_min,ny_min,nx_max,ny_max)
#     img_ = Image.open(image)
#     cropped = img_.crop((nx_min,ny_min,nx_max,ny_max))
#     cropped.show()
#     n = 0
#     for i in range(ny_min,ny_max):
#         for j in range(nx_min,nx_max):
#             print(skin[i][j])
#             if(skin[i][j]==0):
#                 n = n+1
#     nose_masked = n*1.0/((nx_max-nx_min)*(ny_max-ny_min))
#     print(nose_masked)
#     if(nose_masked>=0.7):
#         # return 1
#         print('1')
#     else:
#         # return 0
#         print('0')
#     # if(ex_max1<ex_min2):
#     #     nx_min = ex_max1
#     #     nx_max = ex_min2
#     # else:
#     #     nx_min = ex_max2
#     #     nx_max = ex_min1
#     # if(ey_max1>ey_max2):
#     #     ny_min = int(ey_max1-0.3*(ey_max1-ey_min1))
#     # else:
#     #     ny_min = int(ey_max2-0.3*(ey_max2-ey_min2))
#     # ny_max = int(ny_min+1.3*(ey_max1-ey_min1))
#     # n=0
#     # for i in range(ny_min,ny_max):
#     #     for j in range(nx_min,nx_max):
#     #         if(skin[i][j]==0):
#     #             n = n+1
#     # nose_masked = n*1.0/((nx_max-nx_min)*(ny_max-ny_min))
#     # if(nose_masked>=0.7):
#     #     print('1')
#     # else:
#     #     print('0')
#     # print(skin.shape)
#     # print(skin)
#
#     dst = cv2.bitwise_and(img, img, mask=skin)
#     cv2.namedWindow("seperate", cv2.WINDOW_NORMAL)
#     cv2.imshow("seperate", dst)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#
# # def normal_detect(img, top, left, bottom, right):
# #     cropped = img.crop((left, top, right, bottom))
# #     cropped.save("crop/20.jpg")
# path = 'crop/2.jpg'
# cr_otsu(path)
