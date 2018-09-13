import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from tabs.daily.tab_daily import TabDaily
from tabs.single.tab_single import TabSingle


class MainFrame(QWidget):
    def __init__(self, title):
        QWidget.__init__(self, flags=Qt.Widget)

        self.title = title
        self.setupUI()

    def setupUI(self):
        self.setGeometry(0, 0, 1280, 720)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('icon.png'))
        self.moveWindowsToCenter()

        self.initTabs()

        self.centerLayout = QVBoxLayout(self)
        self.centerLayout.addWidget(self.tabs)
        # self.centerLayout.addStretch(1)
        self.setLayout(self.centerLayout)

    def moveWindowsToCenter(self):
        # geometry of the main window
        qr = self.frameGeometry()
        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()
        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)
        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

    # def createActions(self):
    #     self.actNew = QAction(None, '&New', self,
    #                           statusTip='Create a New File',
    #                           triggered=self.newFile)
    #
    # def createMenus(self):
    #     self.mainMenu = self.menuBar().addMenu('&File')

    def initTabs(self):
        self.tabs = QTabWidget()
        self.tabList = []
        self.tabTitle = ['daily', 'single', 'monthly', 'yearly']

        self.tabList.append(TabDaily())
        self.tabList.append(TabSingle())
        self.tabList.append(QWidget())
        self.tabList.append(QWidget())

        for i in range(len(self.tabList)):
            self.tabs.addTab(self.tabList[i], self.tabTitle[i])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainFrame('Natural Light Data Center')
    window.show()
    app.exec_()
