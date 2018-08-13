from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import Qt


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