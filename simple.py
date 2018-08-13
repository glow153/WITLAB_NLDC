import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QBoxLayout
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot


class Form(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        self.cnt = 0
        self.lb = QLabel(str(self.cnt))
        self.pb = QPushButton('count')

        self.init_widget()

    def init_widget(self):
        self.setWindowTitle('custom signal')
        form_lbx = QBoxLayout(QBoxLayout.TopToBottom, parent=self)
        self.setLayout(form_lbx)

        self.pb.clicked.connect(self.count)
        form_lbx.addWidget(self.lb)
        form_lbx.addWidget(self.pb)

    @pyqtSlot()
    def count(self):
        self.cnt += 1
        self.lb.setText(str(self.cnt))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    form.resize(250, 150)
    form.move(300, 300)
    form.show()
    exit(app.exec_())
