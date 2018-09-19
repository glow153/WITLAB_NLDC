from PyQt5.Qt import (QComboBox, QColor, QTableWidgetItem,
                      QItemEditorCreatorBase)
from PyQt5.QtCore import pyqtProperty, Qt

from model import Singleton


class LinePlotAttr(Singleton):
    def __init__(self):
        self.colorlist = QColor.colorNames()
        self.markerlist = ['.', ',', 'o', 'v', '<', '>', '^',
                           '1', '2', '3', '4', 's', 'p', '*',
                           'h', 'H', '+', 'x', 'D', 'd']
        self.dashlist = ['-', '--', '-.', ':']

    def makeNamedColorList(self):
        return self.colorlist

    def getColorList(self):
        return self.colorlist

    def getMarkerList(self):
        return self.markerlist

    def getDashList(self):
        return self.dashlist


class ColorListEditor(QComboBox):
    def __init__(self, widget=None):
        super(ColorListEditor, self).__init__(widget)

        self.populateList()

    def getColor(self):
        color = self.itemData(self.currentIndex(), Qt.DecorationRole)
        return color

    def setColor(self, color):
        self.setCurrentIndex(self.findData(color, Qt.DecorationRole))

    color = pyqtProperty(QColor, getColor, setColor, user=True)

    def populateList(self):
        for i, colorName in enumerate(QColor.colorNames()):
            color = QColor(colorName)
            self.insertItem(i, colorName)
            self.setItemData(i, color, Qt.DecorationRole)


class ColorListItemEditorCreator(QItemEditorCreatorBase):
    def createWidget(self, parent):
        return ColorListEditor(parent)


class SelectedDataTableModel:
    # color = QColor('#ffffff')
    def __init__(self, date, color, marker, dash):
        self.date = date
        self.color = color
        self.marker = marker
        self.dash = dash
        self.checker = True

        self.makeTableWidgetItem()

    def makeTableWidgetItem(self):
        self.dateItem = QTableWidgetItem(self.date)
        self.colorItem = QTableWidgetItem(self.color)
        self.markerItem = QTableWidgetItem(self.marker)
        self.dashItem = QTableWidgetItem(self.dash)

        self.dateItem.setFlags(Qt.ItemIsUserCheckable)
        self.colorItem.setFlags(Qt.ItemIsEditable)
        self.markerItem.setFlags(Qt.ItemIsEditable)
        self.dashItem.setFlags(Qt.ItemIsEditable)

        self.dateItem.setCheckState(self.checker)

    def getDate(self):
        return self.date

    def getColor(self):
        return self.color

    def getMarker(self):
        return self.marker

    def getDash(self):
        return self.dash

    def getDateItem(self):
        return self.dateItem

    def getColorItem(self):
        return self.colorItem

    def getMarkerItem(self):
        return self.markerItem

    def getDashItem(self):
        return self.dashItem

    def getChecked(self):
        return self.checker

    def setChecked(self, checker):
        self.checker = checker
