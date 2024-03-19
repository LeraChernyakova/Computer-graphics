# Виджет панели управления
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider
from PyQt5.uic.properties import QtCore


class ControlPanel(QWidget):
    weightsChanged = pyqtSignal()

    def __init__(self, weights, parent=None):
        super().__init__(parent)
        lt = QVBoxLayout(self)
        self.setLayout(lt)

        weightsLabel = QLabel('Веса NURB сплайна', self)
        wLabels = [QLabel(f'W{i}') for i in range(weights)]
        self.wSliders = [QSlider(Qt.Orientation.Horizontal) for i in range(weights)]

        for w in [weightsLabel]:
            lt.addWidget(w)

        for i in range(weights):
            lt.addWidget(wLabels[i])
            lt.addWidget(self.wSliders[i])
            self.wSliders[i].valueChanged.connect(lambda: self.weightsChanged.emit())
            self.wSliders[i].setMaximum(100)
            self.wSliders[i].setMinimum(1)

        lt.addStretch()