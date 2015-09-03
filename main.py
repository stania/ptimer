#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import time


class Window(QWidget):
    def __init__(self, *args):
        self.style = \
            "<font style='font-family: Hack; color: blue; font-size:50px; text-shadow: 0 0 3px #F00;'>{0}</font>"
        QWidget.__init__(self, *args)
        self.setLayout(QVBoxLayout())
        self.label = QLabel(self.style.format('time'))
        self.layout().addWidget(self.label)
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(10)
        effect.setOffset(3)
        effect.setColor(Qt.black)
        self.label.setGraphicsEffect(effect)
        # Let the whold window be a glass
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        # I don't know why the code below is needed
        # from ctypes import windll, c_int, byref
        # windll.dwmapi.DwmExtendFrameIntoClientArea(c_int(self.winId()), byref(c_int(-1)))
        self.move(50, 50)

    def mousePressEvent(self, event):
        self.label.setText(self.style.format(time.time()))
        self.repaint()


def main():
    app = QApplication(sys.argv)

    w = Window()
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
