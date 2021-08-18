import gc
import os

import cv2
from PIL import Image
from PyQt5.QtWidgets import QFileDialog
import numpy as np

import yolo
from ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys



class query_window(QtWidgets.QMainWindow):
    # global yolo_
    # yolo_ = yolo.YOLO()
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.yolo_ = yolo.YOLO()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.query_formula)
        self.ui.pushButton_2.clicked.connect(self.query_formula_2)
        self.ui.pushButton_3.clicked.connect(self.query_formula_3)
        self.ui.pushButton_4.clicked.connect(self.query_formula_4)
        # self.ui.pushButton_5.clicked.connect(self.query_formula_5)
        # 给button 的 点击动作绑定一个事件处理函数

    def query_formula(self):
        # 人脸口罩检测图片检测的业务逻辑
        image = QFileDialog.getOpenFileName(self, '选择图片', '', 'Pictures files(*.jpg , *.png)')
        image_ = image[0]
        if image_ == '':
            return
        img = Image.open(image_)
        r_image, hm, nm = self.yolo_.detect_image2(img)
        hm_text = 'number of have_mask: ' + str(hm)
        nm_text = 'number of no_mask: ' + str(nm)
        # result = np.asarray(image)
        width, height = r_image.size
        height = height+70
        new_pic = Image.new('RGB', (width, height))
        data = np.asarray(new_pic)
        cv2.putText(data, text=hm_text, org=(3, 25), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8,
                    color=(0, 255, 0), thickness=2)
        cv2.putText(data, text=nm_text, org=(3, 52), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8,
                    color=(255, 0, 0), thickness=2)
        result_ = np.reshape(data, (height, width, 3))
        img_ = Image.fromarray(result_)
        img_.paste(r_image,(0,70))
        img_.show()

    def query_formula_3(self):
        # 口罩规范佩戴识别图片识别的业务逻辑
        image = QFileDialog.getOpenFileName(self, '选择图片', '', 'Pictures files(*.jpg , *.png)')
        image_ = image[0]
        if image_ == '':
            return
        img = Image.open(image_)
        r_image,mm = self.yolo_.detect_image(img)
        width, height = r_image.size
        height = height + 50
        new_pic = Image.new('RGB', (width, height))
        data = np.asarray(new_pic)
        if mm == 0:
            mm_text = 'no mask! please wear a mask!'
            cv2.putText(data, text=mm_text, org=(3, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.6, color=(255, 0, 0), thickness=2)
        elif mm == 1:
            mm_text = 'masked wrong! please wear a mask properly!'
            cv2.putText(data, text=mm_text, org=(3, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.6, color=(255, 255, 0), thickness=2)
        elif mm == 2:
            mm_text = 'masked well!'
            cv2.putText(data, text=mm_text, org=(3, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.6, color=(0, 255, 0), thickness=2)
        result_ = np.reshape(data, (height, width, 3))
        img_ = Image.fromarray(result_)
        img_.paste(r_image, (0, 50))
        img_.show()

    def query_formula_2(self):
        # 人脸口罩检测视频检测的业务逻辑
        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton_3.setEnabled(False)
        self.ui.pushButton_4.setEnabled(False)
        yolo.detect_video2(self.yolo_, '', '')
        self.ui.pushButton.setEnabled(True)
        self.ui.pushButton_2.setEnabled(True)
        self.ui.pushButton_3.setEnabled(True)
        self.ui.pushButton_4.setEnabled(True)

    def query_formula_4(self):
        # 口罩规范佩戴识别视频检测的业务逻辑
        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton_3.setEnabled(False)
        self.ui.pushButton_4.setEnabled(False)
        yolo.detect_video1(self.yolo_, '', '')
        self.ui.pushButton.setEnabled(True)
        self.ui.pushButton_2.setEnabled(True)
        self.ui.pushButton_3.setEnabled(True)
        self.ui.pushButton_4.setEnabled(True)

    # def query_formula_5(self):
    #     # 口罩规范佩戴识别视频检测的业务逻辑
    #     exit(0)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = query_window()
    window.setStyleSheet("#MainWindow{border-image:url(1.png);}")
    window.show()
    app.exec_()
