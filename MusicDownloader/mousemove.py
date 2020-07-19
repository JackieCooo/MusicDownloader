import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem


class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        self.button_label = QLabel('No Button Pressed', self)  # 1
        self.xy_label = QLabel('x:0, y:0', self)  # 2
        self.global_xy_label = QLabel('global x:0, global y:0', self)  # 3

        self.button_label.setAlignment(Qt.AlignCenter)
        self.xy_label.setAlignment(Qt.AlignCenter)
        self.global_xy_label.setAlignment(Qt.AlignCenter)

        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.button_label)
        self.v_layout.addWidget(self.xy_label)
        self.v_layout.addWidget(self.global_xy_label)
        self.setLayout(self.v_layout)

        self.resize(500, 500)

        self.setMouseTracking(False)  # 4

        self.table_widget = QTableWidget(self)
        self.table_widget.setMouseTracking(True)
        self.table_widget.setRowCount(5)
        self.table_widget.setColumnCount(5)
        self.table_widget.resize(100, 100)
        for i in range(5):
            for j in range(5):
                item = QTableWidgetItem()
                self.table_widget.setItem(i, j, item)
        self.table_widget.setObjectName("tableWidget")

    def mouseMoveEvent(self, QMouseEvent):  # 5
        x = QMouseEvent.x()
        y = QMouseEvent.y()
        print(x)
        print(y)
        global_x = QMouseEvent.globalX()
        global_y = QMouseEvent.globalY()

        self.xy_label.setText('x:{}, y:{}'.format(x, y))
        self.global_xy_label.setText('global x:{}, global y:{}'.format(global_x, global_y))

    def mousePressEvent(self, QMouseEvent):  # 6
        if QMouseEvent.button() == Qt.LeftButton:
            self.button_label.setText('Left Button Pressed')
        elif QMouseEvent.button() == Qt.MidButton:
            self.button_label.setText('Middle Button Pressed')
        elif QMouseEvent.button() == Qt.RightButton:
            self.button_label.setText('Right Button Pressed')

    def mouseReleaseEvent(self, QMouseEvent):  # 7
        if QMouseEvent.button() == Qt.LeftButton:
            self.button_label.setText('Left Button Released')
        elif QMouseEvent.button() == Qt.MidButton:
            self.button_label.setText('Middle Button Released')
        elif QMouseEvent.button() == Qt.RightButton:
            self.button_label.setText('Right Button Released')

    def mouseDoubleClickEvent(self, QMouseEvent):  # 8
        if QMouseEvent.button() == Qt.LeftButton:
            self.button_label.setText('Left Button Double Clikced')
        elif QMouseEvent.button() == Qt.MidButton:
            self.button_label.setText('Middle Button Double Clicked')
        elif QMouseEvent.button() == Qt.RightButton:
            self.button_label.setText('Right Button Double Clikced')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())