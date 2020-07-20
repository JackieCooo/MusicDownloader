import sys
import os
from MusicSource import xiami, migu, netease, qq, kuwo, kugo
from PyQt5 import QtCore, QtGui, QtWidgets


class GUIMainWindow(object):

    def __init__(self):
        self.engine_list = ['网易云音乐', 'QQ音乐', '酷狗音乐', '酷我音乐', '虾米音乐', '咪咕音乐']
        self.sess = None
        self.filename_type = 0
        self.lyric_format_type = 0
        self.music_quality_type = 0
        if not os.path.exists('Downloads'):
            os.mkdir('Downloads')
        self.directory = os.path.split(os.path.realpath(__file__))[0] + "\\Downloads\\"
        print(self.directory)
        self.btn_list = [self.btn_set(i) for i in range(30)]

    def setup_ui(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(1200, 800)
        main_window.setWindowTitle('MusicDownloader - Designed by Jackie')
        main_window.setWindowIcon(QtGui.QIcon('icon.ico'))
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(main_window.sizePolicy().hasHeightForWidth())
        main_window.setSizePolicy(size_policy)
        self.centralwidget = QtWidgets.QWidget(main_window)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(size_policy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(1)
        size_policy.setVerticalStretch(1)
        size_policy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(size_policy)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")

        # 搜索页样式设置
        self.search_tab = QtWidgets.QWidget()
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.search_tab.sizePolicy().hasHeightForWidth())
        self.search_tab.setSizePolicy(size_policy)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.search_tab.setFont(font)
        self.search_tab.setObjectName("search_tab")
        self.search_page = QtWidgets.QGridLayout(self.search_tab)
        self.search_page.setContentsMargins(0, 5, 0, 0)
        self.search_page.setObjectName("search_page")
        self.search_area = QtWidgets.QHBoxLayout()
        self.search_area.setObjectName("search_area")
        self.search_area.setSpacing(0)
        self.search_area.setContentsMargins(10, 0, 10, 0)

        # 搜索引擎切换
        self.engine = QtWidgets.QComboBox(self.search_tab)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(1)
        size_policy.setVerticalStretch(1)
        size_policy.setHeightForWidth(self.engine.sizePolicy().hasHeightForWidth())
        self.engine.setSizePolicy(size_policy)
        self.engine.setFixedHeight(36)
        self.engine.setFrame(True)
        combobox_text = QtWidgets.QLineEdit()  # 设置combobox字体
        combobox_text.setReadOnly(True)
        combobox_text.setAlignment(QtCore.Qt.AlignCenter)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.engine.setPalette(palette)
        self.engine.setLineEdit(combobox_text)
        combobox_drop_down = QtWidgets.QListWidget()  # 设置combobox下拉菜单字体
        for i in range(6):
            item = QtWidgets.QListWidgetItem(self.engine_list[i])
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            combobox_drop_down.addItem(item)
        self.engine.setModel(combobox_drop_down.model())
        self.engine.setView(combobox_drop_down)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setBold(True)
        font.setPointSize(10)
        self.engine.setFont(font)
        self.engine.setObjectName("engine")
        self.engine.setCursor(QtCore.Qt.PointingHandCursor)
        self.engine.currentIndexChanged.connect(self.engine_switch)  # 搜索引擎切换
        self.search_area.addWidget(self.engine)

        # 搜索框
        self.search_name = QtWidgets.QLineEdit(self.search_tab)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(6)
        size_policy.setVerticalStretch(1)
        size_policy.setHeightForWidth(self.search_name.sizePolicy().hasHeightForWidth())
        self.search_name.setSizePolicy(size_policy)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.search_name.setTextMargins(5, 0, 0, 0)
        self.search_name.setFont(font)
        self.search_name.setObjectName("search_name")
        self.search_name.placeholderText()
        self.search_name.setPlaceholderText("输入歌名")
        self.search_name.setCursor(QtCore.Qt.IBeamCursor)
        self.search_area.addWidget(self.search_name)

        # 搜索按钮
        self.search_button = QtWidgets.QPushButton(self.search_tab)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(1)
        size_policy.setVerticalStretch(1)
        size_policy.setHeightForWidth(self.search_button.sizePolicy().hasHeightForWidth())
        self.search_button.setSizePolicy(size_policy)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.search_button.setFont(font)
        self.search_button.setObjectName("search_button")
        self.search_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.search_button.clicked.connect(self.search)  # 搜索按钮
        self.search_area.addWidget(self.search_button)
        self.search_page.addLayout(self.search_area, 0, 0, 1, 1)

        # 搜索结果
        self.search_result = QtWidgets.QTableWidget(self.search_tab)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.search_result.setFont(font)
        self.search_result.setColumnCount(5)
        self.search_result.setRowCount(30)
        self.search_result.setHorizontalHeaderLabels(['歌名', '歌手', '专辑', '时长', '操作'])
        self.search_result.setMouseTracking(True)
        self.search_result.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.search_result.setShowGrid(False)
        self.search_result.setGridStyle(QtCore.Qt.NoPen)
        self.search_result.horizontalHeader().setStretchLastSection(True)
        self.search_result.verticalHeader().setVisible(False)
        self.search_result.horizontalHeader().resizeSection(0, 300)
        self.search_result.horizontalHeader().resizeSection(1, 250)
        self.search_result.horizontalHeader().resizeSection(2, 250)
        self.search_result.horizontalHeader().resizeSection(3, 100)
        self.search_result.setSortingEnabled(True)
        self.search_result.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.search_result.setObjectName("search_result")
        self.search_page.addWidget(self.search_result, 1, 0, 1, 1)
        self.tabWidget.addTab(self.search_tab, "搜索")
        # for i in range(30):
        #     self.search_result.setCellWidget(i, 4, self.btn_list[i])

        # 设置页设置
        self.option_page = QtWidgets.QWidget()
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.option_page.sizePolicy().hasHeightForWidth())
        self.option_page.setSizePolicy(size_policy)
        self.option_page.setObjectName("option_page")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.option_page)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(200, 25, 200, 200)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_1 = QtWidgets.QLabel(self.option_page)
        self.label_1.setObjectName("label_1")
        self.verticalLayout_2.addWidget(self.label_1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.option_page)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.toolButton = QtWidgets.QToolButton(self.option_page)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout_2.addWidget(self.toolButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.label_2 = QtWidgets.QLabel(self.option_page)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.radioButton_1 = QtWidgets.QRadioButton(self.option_page)
        self.radioButton_1.setChecked(True)
        self.radioButton_1.setObjectName("radioButton_1")
        self.buttonGroup_1 = QtWidgets.QButtonGroup(main_window)
        self.buttonGroup_1.setObjectName("buttonGroup_1")
        self.buttonGroup_1.addButton(self.radioButton_1)
        self.horizontalLayout_3.addWidget(self.radioButton_1)
        self.radioButton_2 = QtWidgets.QRadioButton(self.option_page)
        self.radioButton_2.setObjectName("radioButton_2")
        self.buttonGroup_1.addButton(self.radioButton_2)
        self.horizontalLayout_3.addWidget(self.radioButton_2)
        self.radioButton_3 = QtWidgets.QRadioButton(self.option_page)
        self.radioButton_3.setObjectName("radioButton_3")
        self.buttonGroup_1.addButton(self.radioButton_3)
        self.horizontalLayout_3.addWidget(self.radioButton_3)
        spacerItem = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.label_3 = QtWidgets.QLabel(self.option_page)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.radioButton_4 = QtWidgets.QRadioButton(self.option_page)
        self.radioButton_4.setChecked(True)
        self.radioButton_4.setObjectName("radioButton_4")
        self.buttonGroup_2 = QtWidgets.QButtonGroup(main_window)
        self.buttonGroup_2.setObjectName("buttonGroup_2")
        self.buttonGroup_2.addButton(self.radioButton_4)
        self.horizontalLayout_4.addWidget(self.radioButton_4)
        self.radioButton_5 = QtWidgets.QRadioButton(self.option_page)
        self.radioButton_5.setObjectName("radioButton_5")
        self.buttonGroup_2.addButton(self.radioButton_5)
        self.horizontalLayout_4.addWidget(self.radioButton_5)
        spacerItem1 = QtWidgets.QSpacerItem(400, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.label_4 = QtWidgets.QLabel(self.option_page)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.radioButton_6 = QtWidgets.QRadioButton(self.option_page)
        self.radioButton_6.setObjectName("radioButton_6")
        self.buttonGroup_3 = QtWidgets.QButtonGroup(main_window)
        self.buttonGroup_3.setObjectName("buttonGroup_3")
        self.buttonGroup_3.addButton(self.radioButton_6)
        self.horizontalLayout_5.addWidget(self.radioButton_6)
        self.radioButton_7 = QtWidgets.QRadioButton(self.option_page)
        self.radioButton_7.setObjectName("radioButton_7")
        self.buttonGroup_3.addButton(self.radioButton_7)
        self.horizontalLayout_5.addWidget(self.radioButton_7)
        self.radioButton_8 = QtWidgets.QRadioButton(self.option_page)
        self.radioButton_8.setChecked(True)
        self.radioButton_8.setObjectName("radioButton")
        self.horizontalLayout_5.addWidget(self.radioButton_8)
        spacerItem2 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.gridLayout_4.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.option_page, "设置")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.label_1.setText("下载地址：")
        self.toolButton.setText("...")
        self.label_2.setText("命名格式：")
        self.radioButton_1.setText("歌曲名-歌手")
        self.radioButton_2.setText("歌手-歌曲名")
        self.radioButton_3.setText("歌曲名")
        self.label_3.setText("歌词格式：")
        self.radioButton_4.setText(".lrc")
        self.radioButton_5.setText(".txt")
        self.label_4.setText("下载音质：")
        self.radioButton_6.setText("无损音质 >320kbps")
        self.radioButton_7.setText("高品质 320kbps")
        self.radioButton_8.setText("标准音质 160kbps")
        self.buttonGroup_3.addButton(self.radioButton_8)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.radioButton_1.setFont(font)
        self.radioButton_2.setFont(font)
        self.radioButton_3.setFont(font)
        self.radioButton_4.setFont(font)
        self.radioButton_5.setFont(font)
        self.radioButton_6.setFont(font)
        self.radioButton_7.setFont(font)
        self.radioButton_8.setFont(font)
        self.lineEdit_2.setFont(font)
        self.toolButton.clicked.connect(self.choose_directory)

        main_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def engine_switch(self):
        print(f'当前搜索引擎：{self.engine.currentIndex()}')
        if self.engine.currentIndex() == 0:
            self.sess = netease.NeteaseMusic()
        elif self.engine.currentIndex() == 1:
            self.sess = qq.QqMusic()
        elif self.engine.currentIndex() == 2:
            self.sess = kugo.KugoMusic()
        elif self.engine.currentIndex() == 3:
            self.sess = kuwo.KuwoMusic()
        elif self.engine.currentIndex() == 4:
            self.sess = xiami.XiamiMusic()
        elif self.engine.currentIndex() == 5:
            self.sess = migu.MiguMusic()

    def filename_type_choice(self):
        if self.radioButton_1.isChecked():
            self.filename_type = 0
        elif self.radioButton_2.isChecked():
            self.filename_type = 1
        elif self.radioButton_3.isChecked():
            self.filename_type = 2

    def lyric_format_choice(self):
        if self.radioButton_4.isChecked():
            self.lyric_format_type = 0
        elif self.radioButton_5.isChecked():
            self.lyric_format_type = 1

    def music_quality_choice(self):
        if self.radioButton_6.isChecked():
            self.music_quality_type = 0
        elif self.radioButton_7.isChecked():
            self.music_quality_type = 1
        elif self.radioButton_8.isChecked():
            self.music_quality_type = 2

    def search(self):
        search_name = self.search_name.text()
        if search_name == '':
            pass
        else:
            n, res = self.sess.search_music(search_name, 1, 0)
            print(res)
            # print(n)
            self.show_result(res)

    def show_result(self, res):
        self.search_result.setRowCount(30)
        self.search_result.clearContents()
        for i in range(30):
            for j in range(4):
                item = QtWidgets.QTableWidgetItem(res[i][j])
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.search_result.setItem(i, j, item)
            self.search_result.setCellWidget(i, 4, self.btn_list[i])

    def download(self, num):
        song_name = self.search_result.item(num, 0).text()
        artist_name = self.search_result.item(num, 1).text()
        self.statusbar.showMessage(f'正在下载{song_name} - {artist_name}')
        self.sess.download(num + 1, self.filename_type, self.lyric_format_type, self.directory)
        self.statusbar.showMessage(f'{song_name} - {artist_name}下载成功')

    def choose_directory(self):
        self.directory = QtWidgets.QFileDialog.getExistingDirectory(caption='选取文件夹', directory='./') + '/'
        print(self.directory)
        self.lineEdit_2.setText(self.directory)

    def btn_set(self, num):
        download_btn = QtWidgets.QPushButton()
        download_btn.setObjectName("dl_btn")
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHeightForWidth(download_btn.sizePolicy().hasHeightForWidth())
        download_btn.setSizePolicy(size_policy)
        download_btn.resize(25, 25)
        download_btn.setCursor(QtCore.Qt.PointingHandCursor)
        download_btn.clicked.connect(lambda: self.download(num))  # 歌曲下载按钮

        lyric_btn = QtWidgets.QPushButton()
        lyric_btn.setObjectName("lr_btn")
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHeightForWidth(lyric_btn.sizePolicy().hasHeightForWidth())
        lyric_btn.setSizePolicy(size_policy)
        lyric_btn.resize(25, 25)
        lyric_btn.setCursor(QtCore.Qt.PointingHandCursor)
        lyric_btn.clicked.connect(lambda: self.sess.get_song_lyric(num + 1, self.filename_type, self.lyric_format_type, self.directory))  # 歌词下载按钮

        image_btn = QtWidgets.QPushButton()
        image_btn.setObjectName("ig_btn")
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHeightForWidth(image_btn.sizePolicy().hasHeightForWidth())
        image_btn.setSizePolicy(size_policy)
        image_btn.resize(25, 25)
        image_btn.setCursor(QtCore.Qt.PointingHandCursor)
        image_btn.clicked.connect(lambda: self.sess.get_song_cover(num + 1, self.filename_type, self.directory))  # 封面下载按钮

        more_btn = QtWidgets.QPushButton()
        more_btn.setObjectName("mr_btn")
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHeightForWidth(more_btn.sizePolicy().hasHeightForWidth())
        more_btn.setSizePolicy(size_policy)
        more_btn.resize(25, 25)
        more_btn.setCursor(QtCore.Qt.PointingHandCursor)
        # more_btn.clicked.connect()  # 更多选项按钮

        h_1 = QtWidgets.QHBoxLayout()
        h_1.addWidget(download_btn)
        h_1.addWidget(lyric_btn)
        h_1.addWidget(image_btn)
        h_1.addWidget(more_btn)
        h_1.setContentsMargins(20, 0, 20, 0)
        h_1.setSpacing(20)
        op_btn_set = QtWidgets.QWidget()
        op_btn_set.setLayout(h_1)
        return op_btn_set


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    run = GUIMainWindow()
    flag = QtWidgets.QMainWindow()
    run.setup_ui(flag)
    run.engine_switch()
    with open('StyleSheet.qss', 'r') as f:
        style = f.read()
    app.setStyleSheet(style)
    flag.show()
    sys.exit(app.exec_())
