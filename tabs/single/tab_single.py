from PyQt5.QtCore import (Qt, pyqtSlot)
from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QHBoxLayout)
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from tabs.single.select_spird import getSpectra


class TabSingle(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)

        self.btn_drawPlot = QPushButton("차트그리기")
        self.btn_drawPlot.clicked.connect(self.drawSp)

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)

        # Left Layout
        self.leftLayout = QVBoxLayout()
        self.leftLayout.addWidget(self.canvas)

        # Right Layout
        self.rightLayout = QVBoxLayout()
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
        # self.pysparkmgr = PySparkManager()

    @pyqtSlot(name='drawSpectra')
    def drawSp(self):
        date = '2017-04-13'
        time = '124024'
        plt.close()
        self.fig.clear()

        dict_sp = getSpectra(date, time)
        wl = list(dict_sp.keys())
        ird = list(dict_sp.values())

        for i in range(len(wl)):
            wl[i] = float(wl[i].decode('utf-8').split(':')[1])
            ird[i] = float(ird[i].decode('utf-8'))

        print(wl)
        print(ird)
        print('max ird = %f' % max(ird))

        ax = self.fig.add_subplot(111)

        ax.scatter(wl, ird, color='blue',
                   label='%s %s' % (date, time))
        ax.set_ylim(0, max(ird))
        ax.set_xlabel('wavelength [nm]')
        ax.set_ylabel('spectral irradiance [W/m2]')

        ax.legend(loc='upper right', fontsize=10)
        # plt.show()

        self.canvas.draw()
