#!/usr/bin/python
import sys
from GUI import UI
from PyQt4 import QtGui


class MainController:

    def __init__(self):
        application = QtGui.QApplication(sys.argv)
        gui = UI()
        gui.show()
        sys.exit(application.exec_())

    def detect_face(self):
        pass

    def train_algorithm(self):
        pass


def main():

    ui = MainController()


if __name__ == '__main__':
    main()
