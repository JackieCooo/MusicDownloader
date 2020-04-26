import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QApplication, QWidget, QTableView, QAbstractItemView, QLabel, QVBoxLayout


class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        self.resize(650, 300)

        self.model = QStandardItemModel(6, 6, self)  # 1
        # self.model = QStandardItemModel(self)
        # self.model.setColumnCount(6)
        # self.model.setRowCount(6)

        for row in range(6):  # 2
            for column in range(6):
                item = QStandardItem('({}, {})'.format(row, column))
                self.model.setItem(row, column, item)

        self.item_list = [QStandardItem('(6, {})'.format(column)) for column in range(6)]
        # appendRow()方法可以把新行添加到表格最后，也就是说目前有7行
        self.model.appendRow(self.item_list)  # 3

        self.item_list = [QStandardItem('(7, {})'.format(column)) for column in range(6)]
        # insertRow()方法可以在指定方法添加一行，这里我们在最后一行插入一行，现在有8行
        self.model.insertRow(7, self.item_list)  # 4

        self.table = QTableView(self)  # 5
        self.table.setModel(self.model)
        self.table.horizontalHeader().setStretchLastSection(True)
        # self.table.horizontalHeader().setStretchLastSection(True)可以让表格填满整个窗口，如果拉伸窗口的话则为了填满窗口表格最后列会改变尺寸
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # setEditTriggers()方法设置编辑规则，这里我们设置无法编辑。最后将clicked信号和自定义的槽函数连接起来
        self.table.clicked.connect(self.show_info)
        # info_label用于显示单元格文本
        self.info_label = QLabel(self)  # 6
        self.info_label.setAlignment(Qt.AlignCenter)

        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.table)
        self.v_layout.addWidget(self.info_label)
        self.setLayout(self.v_layout)

    def show_info(self):  # 7
        row = self.table.currentIndex().row()
        column = self.table.currentIndex().column()
        print('({}, {})'.format(row, column))

        data = self.table.currentIndex().data()
        self.info_label.setText(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
