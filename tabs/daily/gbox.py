from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QComboBox, QGroupBox, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QLabel, QCheckBox, QLineEdit,
                             QListWidget, QListWidgetItem)
from matplotlib import colors as mcolors

from pysparkmgr import PySparkManager


class GbxDatelist(QGroupBox):
    def __init__(self, title):
        QGroupBox.__init__(self, title)
        self.totalDateListwdg = QListWidget()
        self.itemListwdg_l = QListWidget()
        self.itemListwdg_r = QListWidget()

        self.layout = QHBoxLayout()

        # get date list from dataframe using pyspark
        self.initTotalDateList()

        # set components and layout
        self.setComponentsWithLayout()

    def setComponentsWithLayout(self):
        totaldatelistLayout = QVBoxLayout()
        itemListLayout_l = QVBoxLayout()
        itemListLayout_r = QVBoxLayout()

        # set size
        self.totalDateListwdg.setFixedWidth(120)
        self.itemListwdg_l.setFixedWidth(150)
        self.itemListwdg_r.setFixedWidth(150)

        totaldatelistLayout.addWidget(QLabel('날짜 선택'))
        totaldatelistLayout.addWidget(self.totalDateListwdg)
        itemListLayout_l.addWidget(QLabel('왼쪽 축 데이터'))
        itemListLayout_l.addWidget(self.itemListwdg_l)
        itemListLayout_r.addWidget(QLabel('오른쪽 축 데이터'))
        itemListLayout_r.addWidget(self.itemListwdg_r)

        self.layout.addLayout(totaldatelistLayout, 40)
        self.layout.addLayout(itemListLayout_l, 30)
        self.layout.addLayout(itemListLayout_r, 30)
        self.setLayout(self.layout)

    def initTotalDateList(self):
        pysparkmgr = PySparkManager()
        totaldatelist = pysparkmgr.getDF('nt_srs') \
            .select('date') \
            .sort('date') \
            .distinct() \
            .toPandas().values.tolist()

        totaldatelist = list(map(lambda date: date[0], totaldatelist))

        for dt in totaldatelist:
            item = QListWidgetItem()
            item.setText(dt)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.totalDateListwdg.addItem(item)

    def getDateChecked(self):
        ret = []
        for i in range(self.totalDateListwdg.count()):
            if self.totalDateListwdg.item(i).checkState() == Qt.Checked:
                ret.append(self.totalDateListwdg.item(i).text())
        return ret


class GbxVisual(QGroupBox):
    def __init__(self, title):
        QGroupBox.__init__(self, title)
        # self.setFixedSize(120, 150)

        self.colorlist = self.getNamedColorList()
        self.markerlist = ['.', ',', 'o', 'v', '<', '>', '^',
                           '1', '2', '3', '4', 's', 'p', '*',
                           'h', 'H', '+', 'x', 'D', 'd']
        self.linelist = ['-', '--', '-.', ':']

        self.cbxColor = QComboBox()
        self.cbxMarkerType = QComboBox()
        self.cbxLineType = QComboBox()

        self.layout = QGridLayout()

        self.setItemsInCbx()
        self.setComponentsWithLayout()

        # disable for testmode
        self.cbxColor.setEnabled(False)
        self.cbxMarkerType.setEnabled(False)
        self.cbxLineType.setEnabled(False)

    def getNamedColorList(self):
        # matplotlib color list : named_color.py
        # https://matplotlib.org/examples/color/named_colors.html
        colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
        by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgba(color)[:3])), name)
                        for name, color in colors.items())
        sorted_names = [name for hsv, name in by_hsv]
        return sorted_names

    def setItemsInCbx(self):
        self.cbxColor.addItems(self.colorlist)
        self.cbxMarkerType.addItems(self.markerlist)
        self.cbxLineType.addItems(self.linelist)

    def setComponentsWithLayout(self):
        self.layout.setColumnStretch(1, 2)
        self.layout.setColumnStretch(2, 2)
        self.layout.setColumnStretch(3, 2)

        self.layout.addWidget(QLabel('색상'), 0, 0)
        self.layout.addWidget(self.cbxColor, 0, 1)
        self.layout.addWidget(QLabel('마커'), 1, 0)
        self.layout.addWidget(self.cbxMarkerType, 1, 1)
        self.layout.addWidget(QLabel('선'), 2, 0)
        self.layout.addWidget(self.cbxLineType, 2, 1)

        self.setLayout(self.layout)


class GbxAxis(QGroupBox):
    @staticmethod
    def default_ylim(type):
        if type is 'illum':
            return 140000
        elif type is 'cct':
            return 12000
        elif type is 'swr':
            return 60

    def __init__(self, title):
        QGroupBox.__init__(self, title)
        # self.setFixedSize(120, 150)

        self.leftAxis = ['illum', 'cct', 'swr']
        self.rightAxis = ['illum', 'cct', 'swr']

        self.cbxLeft = QComboBox()
        self.cbxRight = QComboBox()
        self.leLeftLowerLim = QLineEdit('0')
        self.leLeftUpperLim = QLineEdit(str(self.default_ylim('illum')))
        self.leRightLowerLim = QLineEdit()
        self.leRightUpperLim = QLineEdit()

        # init comps
        self.leLeftLowerLim.setFixedWidth(70)
        self.leLeftUpperLim.setFixedWidth(70)
        self.leRightLowerLim.setFixedWidth(70)
        self.leRightUpperLim.setFixedWidth(70)

        self.chkEnableRightAxis = QCheckBox('오른쪽 축')

        self.layout = QHBoxLayout()

        self.chkEnableRightAxis.setChecked(False)
        self.cbxRight.setEnabled(False)
        self.leRightLowerLim.setEnabled(False)
        self.leRightUpperLim.setEnabled(False)

        self.setItemsInCbx()
        self.setComponentsWithLayout()

        self.chkEnableRightAxis.stateChanged.connect(self.enableRightAxis)
        self.cbxLeft.currentTextChanged.connect(self.initLeYlim_left)
        self.cbxRight.currentTextChanged.connect(self.initLeYlim_right)

    def setItemsInCbx(self):
        self.cbxLeft.addItems(self.leftAxis)
        self.cbxRight.addItems(self.rightAxis)

    def setComponentsWithLayout(self):
        leftLayout = QVBoxLayout()
        rightLayout = QGridLayout()

        leftLayout.addWidget(QLabel('     '))
        leftLayout.addWidget(QLabel('왼쪽 축'))
        leftLayout.addWidget(self.chkEnableRightAxis)

        rightLayout.setColumnStretch(1, 2)
        rightLayout.setColumnStretch(2, 2)
        rightLayout.setColumnStretch(3, 2)

        rightLayout.addWidget(QLabel('항목'), 0, 0)
        rightLayout.addWidget(QLabel('Y축 상한값'), 0, 1)
        rightLayout.addWidget(QLabel('Y축 하한값'), 0, 2)
        rightLayout.addWidget(self.cbxLeft, 1, 0)
        rightLayout.addWidget(self.leLeftLowerLim, 1, 1)
        rightLayout.addWidget(self.leLeftUpperLim, 1, 2)
        rightLayout.addWidget(self.cbxRight, 2, 0)
        rightLayout.addWidget(self.leRightLowerLim, 2, 1)
        rightLayout.addWidget(self.leRightUpperLim, 2, 2)

        self.layout.addLayout(leftLayout)
        self.layout.addLayout(rightLayout)
        self.layout.setStretchFactor(leftLayout, 0)
        self.layout.setStretchFactor(rightLayout, 1)
        self.setLayout(self.layout)

    def getSelectedItem(self):
        if self.chkEnableRightAxis.isChecked():
            return [str(self.cbxLeft.currentText()), str(self.cbxRight.currentText())]
        else:
            return [str(self.cbxLeft.currentText())]

    # signals from here
    def enableRightAxis(self):
        if self.chkEnableRightAxis.isChecked():
            self.cbxRight.setEnabled(True)
            self.leRightLowerLim.setEnabled(True)
            self.leRightUpperLim.setEnabled(True)
        else:
            self.cbxRight.setEnabled(False)
            self.leRightLowerLim.setEnabled(False)
            self.leRightUpperLim.setEnabled(False)

    def initLeYlim_left(self, type):
        self.leLeftLowerLim.text = '0'
        self.leLeftUpperLim.text = str(self.default_ylim(type))

    def initLeYlim_right(self, type):
        self.leRightLowerLim.text = '0'
        self.leRightUpperLim.text = str(self.default_ylim(type))


class GbxFilter(QGroupBox):
    def __init__(self, title):
        QGroupBox.__init__(self, title)
        # self.setFixedSize(120, 150)
        self.setCheckable(True)
        self.setChecked(False)

        self.filterTypeList = ['jake\'s filter']

        self.cbxFilterType = QComboBox()
        self.layout = QHBoxLayout()

        self.setItemsInCbx()
        self.setComponentsWithLayout()

    def setItemsInCbx(self):
        self.cbxFilterType.addItems(self.filterTypeList)

    def setComponentsWithLayout(self):
        # self.layout.addWidget(self.chkEnableFilter)
        self.layout.addWidget(QLabel('필터링 알고리즘'))
        self.layout.addWidget(self.cbxFilterType)
        self.layout.addStretch(1)
        self.setLayout(self.layout)

    def getFilterType(self):
        return self.cbxFilterType.currentIndex()
