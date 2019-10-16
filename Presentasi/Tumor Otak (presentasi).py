import sys
import cv2
import math
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import  QImage,QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow,QFileDialog,QAction
from PyQt5.uic import loadUi
import numpy as np
from tkinter import messagebox
from matplotlib import pyplot as plt

class ShowImage(QMainWindow):
    def __init__(self):
        super(ShowImage, self).__init__()
        loadUi('Tumor Otak (presentasi).ui', self)
        self.image = None
        self.btnload.clicked.connect(self.loadClicked)
        self.actionGreyscale.triggered.connect(self.greyscaleClicked)
        self.actionThresholding.triggered.connect(self.thresholdClicked)
        self.btnreset.clicked.connect(self.reset)
        self.btnhasil.clicked.connect(self.gabunganClicked)

    def reset(self):
        window.destroy()
        self.loadClicked()
        window.show()

    @pyqtSlot()
    def loadClicked(self):
        #self.loadImage('Otak 1.jpg')
        flname,filter = QFileDialog.getOpenFileName(self,'Open File','D:\Kuliah\Semester 6\PCD\Lab\Projek\Program\Presentasi',"Image Files(*.jpg)")
        if flname:
            self.loadImage(flname)
        else:
            print('Invalid Image')

    def loadImage(self, flname):
        self.image = cv2.imread(flname)
        self.displayImage(1)
    @pyqtSlot()
    def greyscaleClicked(self):
        H, W = self.image.shape[:2]
        gray = np.zeros((H, W), np.uint8)
        for i in range(H):
            for j in range(W):
                gray[i, j] = np.clip(
                    0.299 * self.image[i, j, 0] + 0.587 * self.image[i, j, 1] + 0.114 * self.image[i, j, 2], 0, 255)
        self.image = gray
        self.displayImage(3)
        cv2.imwrite("D:\Kuliah\Semester 6\PCD\Lab\Projek\Program\greyscale.jpg", self.image)

    def thresholdClicked(self):
        self.image = cv2.imread("D:\Kuliah\Semester 6\PCD\Lab\Projek\Program\greyscale.jpg")
        img = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        t = 195
        h, w = img.shape[:2]
        for i in np.arange(h):
            for j in np.arange(w):
                b = img.item(i, j)
                if b > t:
                    b = 1
                elif b < t:
                    b = 0
                else:
                    b = b
                b = math.ceil(255 - b)
                img.itemset((i, j), b)
        self.image = img
        self.displayImage(2)
        cv2.imwrite("D:\Kuliah\Semester 6\PCD\Lab\Projek\Program\Threshold.jpg", self.image)

    def gabunganClicked(self):
        #flname,= QFileDialog.getOpenFileName(self, 'Open File', 'E:\\', "Image Files(*.jpg)")
        H, W = self.image.shape[:2]
        gray = np.zeros((H, W), np.uint8)
        for i in range(H):
            for j in range(W):
                gray[i, j] = np.clip(
                    0.299 * self.image[i, j, 0] + 0.587 * self.image[i, j, 1] + 0.114 * self.image[i, j, 2], 0, 255)
        self.image = gray
        img = self.image
        t = 195
        h, w = img.shape[:2]
        for i in np.arange(h):
            for j in np.arange(w):
                b = img.item(i, j)
                if b > t:
                    b = 0
                elif b < t:
                    b = 255
                else:
                    b = b
               
                img.itemset((i, j), b)
        self.image = img

        self.displayImage(4)

        h, w = img.shape[:2]
        hasil = 0
        for i in np.arange(h):
            for j in np.arange(w):
                if (img.item(i, j) == 0):
                    hasil = hasil + 1
        print(hasil)
        if hasil >= 800:
            status = 'Tumor'
        else:
            status = 'Normal'
        print(status)
        messagebox.showinfo(title="Hasil Deteksi", message=status)

    def displayImage(self, windows):
        qformat = QImage.Format_Indexed8
        if len(self.image.shape) == 3:
            if (self.image.shape[2]) == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(self.image, self.image.shape[1], self.image.shape[0], self.image.strides[0], qformat)
        img = img.rgbSwapped()
        if windows == 1:
            self.label_asli.setPixmap(QPixmap.fromImage(img))
            self.label_asli.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            self.label_asli.setScaledContents(True)
        if windows == 2:
            self.label_Threshold.setPixmap(QPixmap.fromImage(img))
            self.label_Threshold.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            self.label_Threshold.setScaledContents(True)
        if windows == 3:
            self.label_gray.setPixmap(QPixmap.fromImage(img))
            self.label_gray.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            self.label_gray.setScaledContents(True)
        if windows == 4:
            self.label_hasil.setPixmap(QPixmap.fromImage(img))
            self.label_hasil.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            self.label_hasil.setScaledContents(True)

app = QtWidgets.QApplication(sys.argv)
window = ShowImage()
window.setWindowTitle('Show Image GUI')
window.show()
sys.exit(app.exec_())
