from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import colors as mcolors

from pysparkmgr.pysparkmgr import PySparkManager

import numpy as np


class DateList(QListWidget):

    def __init__(self, parent):
        QListWidget.__init__(self, parent)
        self.setFixedSize(120, 100)
        self.datelabellist = ['2017-06-02', '2017-10-28']
        self.setMinimumWidth(self.sizeHintForColumn(0))

    def makeList(self):
        for dt in self.datelabellist:
            item = QListWidgetItem()
            item.setText(dt)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.addItem(item)

    def getLabelList(self):
        return self.datelabellist

    def getItemChecked(self):
        ret = []
        for index in range(self.count()):
            if self.item(index).checkState() == Qt.Checked:
                ret.append(self.item(index).text())
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
        self.layout = QVBoxLayout()

        self.setItemsInCbx()
        self.setComponentsWithLayout()

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
        self.layout.addWidget(self.cbxColor)
        self.layout.addWidget(self.cbxMarkerType)
        self.layout.addWidget(self.cbxLineType)
        self.layout.addStretch(1)
        self.setLayout(self.layout)


class GbxFactor(QGroupBox):
    def __init__(self):
        QGroupBox.__init__(self)
        pass


class TabDaily(QWidget):

    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)

        # init components
        self.lbl_conf = QLabel()
        self.lbl_selectDay = QLabel('날짜 입력')
        self.btn_drawPlot = QPushButton("차트그리기")
        self.btn_drawPlot.clicked.connect(self.drawLinePlot)

        self.fig = plt.Figure()
        self.fig.tight_layout()
        self.canvas = FigureCanvas(self.fig)

        # Left Layout
        self.leftLayout = QVBoxLayout()
        self.leftLayout.addWidget(self.canvas)

        # Right Layout
        self.rightLayout = QVBoxLayout()
        self.datelist = DateList(self)
        self.datelist.makeList()
        self.gbxVisual = GbxVisual('선 종류')
        self.rightLayout.addWidget(self.lbl_selectDay)
        self.rightLayout.addWidget(self.datelist)
        self.rightLayout.addWidget(self.gbxVisual)
        self.rightLayout.addWidget(self.btn_drawPlot)
        self.rightLayout.addStretch(1)

        # Main Layout
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.leftLayout)
        self.mainLayout.addLayout(self.rightLayout)
        self.mainLayout.setStretchFactor(self.leftLayout, 1)
        self.mainLayout.setStretchFactor(self.rightLayout, 0)

        self.setLayout(self.mainLayout)

        # get PySparkManager
        self.pysparkmgr = PySparkManager.instance()

    @pyqtSlot(name='drawPlot')
    def drawLinePlot(self):
        plt.close()
        self.fig.clear()

        daylist = self.datelist.getItemChecked()

        for day in daylist:
            df = self.pysparkmgr.getSqlContext()\
                                .read.parquet('hdfs:///ds/nt.parquet')
            rise = self.pysparkmgr.getsrs(day)['rise']
            set = self.pysparkmgr.getsrs(day)['set']

            sel = df.filter('date == "%s"' % day) \
                    .filter('time >= "%s"' % rise) \
                    .filter('time <= "%s"' % set)

            illum = sel.select('illum') \
                       .toPandas()\
                       .values

            cct = sel.select('cct') \
                     .toPandas()\
                     .values

            hmseq = sel.select('time') \
                       .toPandas()\
                       .values

            hmlist = [x[0] for x in hmseq]
            xtick_list = []
            xticklabel_list = []
            for i in range(0, len(hmlist)):
                if hmlist[i].split(':')[1] == '00':
                    xtick_list.append(i)
                    xticklabel_list.append(hmlist[i].split(':')[0])

            ax1 = self.fig.add_subplot(111)
            ax2 = ax1.twinx()

            ax1.plot(np.arange(len(hmseq)), illum, color='blue', label='illum')
            ax2.plot(np.arange(len(hmseq)), cct, color='red', label='cct')

            ax1.set_xticks(xtick_list)
            ax1.set_xticklabels(xticklabel_list)

            ax1.set_ylim(0, (int(max(illum) / 10000) + 1) * 10000)
            ax2.set_ylim(0, 12000)

            ax1.set_xlabel('time')
            ax1.set_ylabel('illum')
            ax2.set_ylabel('cct')

            # plt.show()

            self.canvas.draw()
