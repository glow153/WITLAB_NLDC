import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from tabs.daily.tab_daily import TabDaily


class MainFrame(QWidget):
    def __init__(self, title):
        QWidget.__init__(self, flags=Qt.Widget)

        self.title = title
        self.tabs = QTabWidget()
        self.tabList = []
        self.tabTitle = ['single', 'daily', 'monthly', 'yearly']
        self.setupUI()

    def setupUI(self):
        self.setGeometry(0, 0, 1280, 720)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('icon.png'))
        self.center()

        self.tabList.append(QWidget())
        self.tabList.append(TabDaily())
        self.tabList.append(QWidget())
        self.tabList.append(QWidget())

        for i in range(len(self.tabList)):
            self.tabs.addTab(self.tabList[i], self.tabTitle[i])

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainFrame('Natural Light Data Center v0.1.0')
    window.show()
    app.exec_()
