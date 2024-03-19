import numpy as np
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout

from GLScene import GLScene


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        #Инициализация экрана
        self.init_layout()
        #
        # # Задаём рендер-функцию
        # self.gl_widget.function = self.renderFunction

        # Задаём узловой вектор
        self.T = np.array([
            0, 0, 0,
            np.pi / 2, np.pi / 2,
            np.pi, np.pi,
            3 * np.pi / 2, 3 * np.pi / 2,
            np.pi * 2, np.pi * 2, np.pi * 2
        ]) / (2 * np.pi)

    def init_layout(self):
        self.setGeometry(100, 100, 800, 600)
        self.central_widget = QWidget()
        self.layout = QHBoxLayout()
        self.vertical_layout = QVBoxLayout()
        self.layout.addLayout(self.vertical_layout)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.gl_widget = GLScene()
        self.layout.addWidget(self.gl_widget)

