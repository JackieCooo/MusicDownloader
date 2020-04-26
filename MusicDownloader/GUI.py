# from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFrame, QHBoxLayout, QLineEdit, QSizePolicy, QPushButton
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import sys


class MusicDownloaderGUI(QMainWindow):

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.init_gui()

    def init_gui(self):
        main_window = QMainWindow()
        main_window.resize(900, 600)
        main_window.setWindowTitle('MusicDownloader')
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(1)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(main_window.sizePolicy().hasHeightForWidth())
        main_window.setSizePolicy(size_policy)
        central_widget = QWidget(main_window)
        search_section_widget = QWidget(central_widget)
        search_section_widget.setGeometry(QtCore.QRect(0, 0, 900, 60))
        search_section = QHBoxLayout(search_section_widget)
        search_box = QLineEdit(search_section_widget)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(6)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(search_box.sizePolicy().hasHeightForWidth())
        search_box.setSizePolicy(size_policy)
        search_section.addWidget(search_box)
        search_button = QPushButton(search_section_widget)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(1)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(search_button.sizePolicy().hasHeightForWidth())
        search_button.setSizePolicy(size_policy)
        search_section.addWidget(search_button)
        main_window.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    run = MusicDownloaderGUI()
