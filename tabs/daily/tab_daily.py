import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from pysparkmgr.pysparkmgr import PySparkManager
from tabs.daily.gbox_linetype import GbxVisual
from tabs.daily.listwdg_datelist import DateList


class TabDaily(QWidget):

    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)

        # init components
        self.lbl_conf = QLabel()
        self.lbl_selectDay = QLabel('날짜 입력')
        self.btn_drawPlot = QPushButton("차트그리기")
        self.btn_drawPlot.clicked.connect(self.drawLinePlot)

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)

        # Left Layout
        self.leftLayout = QVBoxLayout()
        self.leftLayout.addWidget(self.canvas)

        # Right Layout
        self.rightLayout = QVBoxLayout()
        self.datelist = DateList(self, self.getDatelist())
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
        self.pysparkmgr = PySparkManager()

    def getDatelist(self):
        pysparkmgr = PySparkManager()
        df = pysparkmgr.getSqlContext() \
            .read.parquet('hdfs:///ds/nt_srs.parquet')
        datelist = df.select('date').sort('date').distinct().toPandas().values.tolist()
        return list(map(lambda date: date[0], datelist))

    @pyqtSlot(name='drawPlot')
    def drawLinePlot(self):
        # reset plot
        plt.close()
        self.fig.clear()

        daylist = self.datelist.getItemChecked()

        for day in daylist:
            df = self.pysparkmgr.getSqlContext() \
                .read.parquet('hdfs:///ds/nt_srs.parquet')

            sel = df.filter('date == "%s"' % day)

            illum = sel.select('illum') \
                       .toPandas()\
                       .values

            cct = sel.select('cct') \
                     .toPandas()\
                     .values

            timelist = sel.select('time') \
                .toPandas() \
                .values

            hmlist = [x[0] for x in timelist]
            xtick_list = []
            xticklabel_list = []
            for i in range(0, len(hmlist)):
                if hmlist[i].split(':')[1] == '00':
                    xtick_list.append(i)
                    xticklabel_list.append(hmlist[i].split(':')[0])

            ax1 = self.fig.add_subplot(111)
            ax2 = ax1.twinx()

            ax1.plot(np.arange(len(timelist)), illum, color='blue', label='illum')
            ax2.plot(np.arange(len(timelist)), cct, color='red', label='cct')

            ax1.set_xticks(xtick_list)
            ax1.set_xticklabels(xticklabel_list)

            ax1.set_ylim(0, (int(max(illum) / 10000) + 1) * 10000)
            ax2.set_ylim(0, 12000)

            ax1.set_xlabel('time')
            ax1.set_ylabel('illum')
            ax2.set_ylabel('cct')

            # plt.show()

            self.canvas.draw()

    def makeTimeline(self, ax, timelist):
        hmlist = [x[0] for x in timelist]
        xtick_list = []
        xticklabel_list = []
        for i in range(0, len(hmlist)):
            if hmlist[i].split(':')[1] == '00':
                xtick_list.append(i)
                xticklabel_list.append(hmlist[i].split(':')[0])
