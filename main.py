#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import time
import pyhk
import threading


class Window(QWidget):
    def __init__(self, *args):
        self.hk = pyhk.pyhk()
        self.hk.addHotkey(['Ctrl', 'Alt', '2'], self.on_hotkey_ca2)

        self.style = \
            "<font style='font-family: Hack; color: #aaaaff; font-size:50px;'>{0}</font>"
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
        self.setMouseTracking(True)
        self.label.setMouseTracking(True)
        self.label.setAttribute(Qt.WA_TransparentForMouseEvents)
        # I don't know why the code below is needed
        # from ctypes import windll, c_int, byref
        # windll.dwmapi.DwmExtendFrameIntoClientArea(c_int(self.winId()), byref(c_int(-1)))
        self.move(50, 50)
        self.ldown = False

    def on_hotkey_ca2(self):
        self.label.setText(self.style.format(time.time()))
        self.repaint()

    def mousePressEvent(self, event):
        """
        :type event: QMouseEvent
        """
        print 'buttons', event.buttons()
        if event.buttons() & Qt.LeftButton:
            self.ldown = True
            self.mpos = event.pos()

    def mouseMoveEvent(self, event):
        """
        :type event: QMouseEvent
        """
        if event.buttons() == Qt.LeftButton:
            diff = event.pos() - self.mpos
            newpos = self.pos() + diff
            self.move(newpos)
        pass

    def mouseReleaseEvent(self, event):
        """
        :type event: QMouseEvent
        """
        self.ldown = False
        print 'ldown = False'
        self.label.setText(self.style.format(time.time()))
        self.repaint()


app = None
win = None


def main():
    global app, win
    app = QApplication(sys.argv)
    win = Window()
    win.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
