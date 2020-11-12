#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Create a UI to promote rapid testing of dex-entry script.

Todo:
    Allow script choice in future maybe
    Variable control
    Advanced script output design/planning?

"""

from PyQt5 import QtWidgets  # type: ignore
from PyQt5.QtWidgets import QApplication, QMainWindow  # type: ignore
from PyQt5.QtGui import QPixmap  # type: ignore
import sys
import subprocess


class OutputChecker(QtWidgets.QWidget):
    def __init__(self, *args):
        super().__init__(*args)
        self.init_ui()

    def init_ui(self):
        self.image_label = QtWidgets.QLabel(self)
        self.pixmap = QPixmap("last_display.png")
        self.image_label.setPixmap(self.pixmap)

        run_button = QtWidgets.QPushButton("Update output")
        run_button.clicked.connect(self.update_image)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(run_button)
        vbox.setContentsMargins(10, 10, 10, 10)

        self.setLayout(vbox)
        self.setFixedSize(vbox.sizeHint())

    def update_image(self):
        subprocess.call(["python", "./dex-entry.py"])
        self.pixmap = QPixmap("last_display.png")
        self.image_label.setPixmap(self.pixmap)


def window() -> None:
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(400, 400, 212, 250)
    win.setWindowTitle("Testing UI")

    output = OutputChecker(win)
    print(output.sizeHint())
    # print(output.margin())

    win.setFixedSize(output.sizeHint())
    win.setStyleSheet("QMainWindow {background: 'gray';}")

    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    window()
