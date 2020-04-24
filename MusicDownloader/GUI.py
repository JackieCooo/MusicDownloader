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
        central_widget = QWidget(main_window)
        search_section = QHBoxLayout()
        search_section.setGeometry(QtCore.QRect(0, 0, 900, 60))
        search_box = QLineEdit(central_widget)
        search_button = QPushButton(central_widget)
        search_section.addWidget(search_box)
        search_section.addWidget(search_button)
        self.setLayout(search_section)
        main_window.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    run = MusicDownloaderGUI()
