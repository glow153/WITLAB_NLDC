from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QListWidgetItem


class DateList(QListWidget):

    def __init__(self, parent):
        QListWidget.__init__(self, parent)
        # self.setFixedSize(120, 100)
        self.setMaximumWidth(200)
        self.setMaximumHeight(150)
        self.setMinimumWidth(self.sizeHintForColumn(0))
        self.datelabellist = ['2017-06-02', '2017-10-28']

    def makeList(self):
        for dt in self.datelabellist:
            item = QListWidgetItem()
            item.setText(dt)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.addItem(item)

        # add signal of doubleclick item
        # for i in range(self.size()):
        #     self.doubleClicked.connect()

    def getLabelList(self):
        return self.datelabellist

    def getItemChecked(self):
        ret = []
        for index in range(self.count()):
            if self.item(index).checkState() == Qt.Checked:
                ret.append(self.item(index).text())
        return ret
