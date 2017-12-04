#!/usr/bin/python
import sys
import cv2
import numpy as np
from PyQt4 import QtGui, QtCore
import MainController


class UI(QtGui.QMainWindow):

    def __init__(self):
        super(UI, self).__init__()

        self.setGeometry(250, 50, 900, 600)
        self.setWindowTitle("FYP-Face Recognition Prototype")
        self.controller = MainController.MainController()

        self.box = QtGui.QWidget()
        self.videoFrame = QtGui.QLabel(self.box)
        self.videoFrame.setGeometry(QtCore.QRect(40, 32, 821, 511))
        self.setCentralWidget(self.box)
        self.videoFrame.setStyleSheet("background-color:black;")

        file_action = QtGui.QAction("&Exit", self)
        file_action.setShortcut("Ctrl+Q")
        file_action.setStatusTip("Leave The App")
        file_action.triggered.connect(self.close_app)
        help_action = QtGui.QAction("&About", self)

        self.statusBar()

        main_menu = self.menuBar()
        file_menu = main_menu.addMenu("&File")
        file_menu.addAction(file_action)

        help_menu = main_menu.addMenu("&Help")
        help_menu.addAction(help_action)

        self.btn_scan = QtGui.QPushButton('Scan', self)
        self.btn_train = QtGui.QPushButton('Train', self)
        self.btn_quit = QtGui.QPushButton('Quit', self)
        self.click_buttons()

    def process_video(self):
        try:
            self.video.capture_frames()
            self.videoFrame.setPixmap(
                self.video.decode())
        except TypeError:
            print("Frame Error")

    def click_buttons(self):

        self.btn_train.clicked.connect(self.train)
        self.btn_train.resize(self.btn_train.sizeHint())
        self.btn_train.move(410, 545)

        self.btn_scan.clicked.connect(self.scan)
        self.btn_scan.resize(self.btn_scan.sizeHint())
        self.btn_scan.move(810, 545)

        self.btn_quit.clicked.connect(self.close_app)
        self.btn_quit.resize(self.btn_quit.sizeHint())
        self.btn_quit.move(5, 545)

    def close_app(self):

        self.video_capture.release()
        cv2.destroyAllWindows()
        sys.exit()

    def scan(self):

        self.btn_train.setDisabled(True)
        self.video_capture = cv2.VideoCapture(0)
        self.video = Video(self.video_capture)
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.process_video)
        self._timer.start(10)
        self.update()

    def train(self):

        self.controller.process_images("/home/patryk/Desktop/pictures")


class Video:
    def __init__(self, capture):
        self.capture = capture
        self.frame = np.array([])
        self.faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    def capture_frames(self):

        ret, self.readFrame = self.capture.read()

        if ret:
            self.frame = cv2.cvtColor(self.readFrame, cv2.COLOR_BGR2RGB)  # cv2.COLOR_BGR2GRAY
            self.gray = cv2.cvtColor(self.readFrame, cv2.COLOR_BGR2GRAY)  # cv2.COLOR_BGR2GRAY

            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            self.gray = clahe.apply(self.gray)

    def decode(self):

        faces = self.faceCascade.detectMultiScale(
            self.gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            # flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.waitKey(0)

        try:
            height, width = self.frame.shape[:2]
            img = QtGui.QImage(self.frame,
                               width,
                               height,
                               QtGui.QImage.Format_RGB888)

            img = QtGui.QPixmap.fromImage(img)
            return img
        except:
            return None


def main():

    application = QtGui.QApplication(sys.argv)
    gui = UI()
    gui.show()
    sys.exit(application.exec_())


if __name__ == '__main__':
    main()