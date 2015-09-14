#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import time
import pyhk

class Config(object):
    COLOR_NORMAL = '#aaaaff'
    COLOR_ALARM_FG = '#ff0000'


class Pomodoro(object):
    PAUSE = 0
    FOCUS = 1
    FOCUS_OVER = 2
    DISTRACTION = 3
    DISTRACTION_OVER = 4

    def __init__(self):
        self.state = Pomodoro.PAUSE
        self.last_update = 0
        self.min = 0
        self.sec = 0
        self.state_length = 0
        self.state_started = 0

    def update(self):
        if self.state in [Pomodoro.FOCUS, Pomodoro.DISTRACTION]:
            time_left = (self.state_started + self.state_length) - time.time()
            self.min = int(time_left) / 60
            self.sec = int(time_left) % 60
            if time_left <= 0:
                # move on to OVER state
                self.state += 1

    def start_focus(self):
        self.state = Pomodoro.FOCUS
        self.state_started = time.time()
        self.state_length = 25 * 60
        ## for debug
        #self.state_length = 5
        self.update()
        print 'focus started'

    def on_distraction(self):
        self.state = Pomodoro.DISTRACTION
        self.state_started = time.time()
        self.state_length = 5 * 60
        ## for debug
        #self.state_length = 5
        self.update()
        print 'distracted!'


class Window(QWidget):
    def __init__(self, *args):
        '''
        :type palette: QPalette
        '''
        QWidget.__init__(self, *args)

        # setup global hotkeys
        self.hk = pyhk.pyhk()
        self.reinstall_hook()

        # init pomodoro state
        self.pomodoro = Pomodoro()

        # Let the whole window be a glass
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        # label styling
        self.format = "{0:02d}:{1:02d}"
        self.setLayout(QVBoxLayout())
        self.label = QLabel()
        self.default_style = {
            'ff': 'Hack',
            'fg': Config.COLOR_NORMAL,
            'size': '50px'
        }
        self.stylesheet = '''
                QLabel {{
                    font-family: {ff};
                    color: {fg};
                    font-size: {size};
                }}
                '''
        computed_style = self.stylesheet.format(**self.default_style);
        print computed_style
        self.label.setStyleSheet(computed_style)
        self.layout().addWidget(self.label)
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(10)
        effect.setOffset(3)
        effect.setColor(Qt.black)
        self.label.setGraphicsEffect(effect)
        # make mouse move event propagated to parent widget
        self.label.setAttribute(Qt.WA_TransparentForMouseEvents)
        # I don't know why the code below is needed
        # from ctypes import windll, c_int, byref
        # windll.dwmapi.DwmExtendFrameIntoClientArea(c_int(self.winId()), byref(c_int(-1)))
        self.move(50, 50)
        self.ldown = False
        self.startTimer(100)

    def reinstall_hook(self):
        self.hk.removeHotkey()
        self.hkid_focus = self.hk.addHotkey(['Ctrl', 'Alt', '1'], self.on_focus)
        self.hkid_dist = self.hk.addHotkey(['Ctrl', 'Alt', '2'], self.on_distraction)

    def on_focus(self):
        self.pomodoro.start_focus()

    def on_distraction(self):
        self.pomodoro.on_distraction()

    def update(self):
        min = self.pomodoro.min
        sec = self.pomodoro.sec
        self.label.setText(self.format.format(min, sec))
        gap = int(time.time() - self.pomodoro.state_started)
        if self.pomodoro.state in [Pomodoro.FOCUS_OVER, Pomodoro.DISTRACTION_OVER] and gap % 2 == 1:
            blinkstyle = self.default_style.copy()
            blinkstyle['fg'] = Config.COLOR_ALARM_FG
            self.label.setStyleSheet(self.stylesheet.format(**blinkstyle))
        else:
            self.label.setStyleSheet(self.stylesheet.format(**self.default_style))
        self.repaint()

    def timerEvent(self, event):
        """
        :type event: QTimerEvent
        """
        self.pomodoro.update()
        self.update()

    def mousePressEvent(self, event):
        """
        :type event: QMouseEvent
        """
        print 'buttons', event.buttons()
        if event.buttons() & Qt.LeftButton:
            self.ldown = True
            self.mpos = event.pos()
            self.reinstall_hook()

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
        pass


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
