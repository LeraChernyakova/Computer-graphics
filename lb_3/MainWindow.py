import numpy as np
from OpenGL.raw.GL.VERSION.GL_1_0 import glPointSize, glLineWidth, glBegin, glColor3dv, glEnd, glVertex2dv, GL_POINTS, \
    GL_LINE_STRIP
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSplitter

from ControlPanel import ControlPanel
from GLScene import GLScene
from drawing import buildNurbs


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Инициализация экрана
        self.init_layout()
        #
        # Задаём рендер-функцию
        self.gl_widget.function = self.renderFunction

        # Опорные точки
        self.P = [
            np.array([0, 0]),
            np.array([1, 3]),
            np.array([2, 1]),
            np.array([3, 4]),
            np.array([4, 0])
        ]

        # Задаём узловой вектор
        self.T = np.arange(len(self.P) + 4)

        # Виджет управления
        self.control = ControlPanel(len(self.P), self)

        # # Задаём начальные веса
        for i in range(5):
            if i % 2 == 0:
                self.control.wSliders[i].setValue(60)
            else:
                self.control.wSliders[i].setValue(int(60 / (2 ** (1 / 2))))

        self.onWeightsChanged()
        self.control.weightsChanged.connect(self.onWeightsChanged)

        sp = QSplitter(self)
        sp.addWidget(self.gl_widget)
        sp.addWidget(self.control)
        sp.setStretchFactor(0, 1)
        self.setCentralWidget(sp)
        self.resize(800, 600)

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

    def onWeightsChanged(self):
        self.W = [s.value() for s in self.control.wSliders]
        self.rebuildSpline()

    # Сборка сплайна
    def rebuildSpline(self):
        self.F, N = buildNurbs(self.T, self.P, self.W)
        X = np.linspace(0, 1, 100)
        self.Points = [self.F(x) for x in X]
        self.redraw()

    def renderFunction(self):
        glPointSize(10)
        glLineWidth(5)
        glBegin(GL_LINE_STRIP)
        glColor3dv((0, 0, 0))
        for p in self.Points:
            glVertex2dv(p)
        glEnd()
        glBegin(GL_POINTS)
        glColor3dv((1, 0, 0))
        for p in self.P:
            glVertex2dv(p)
        glEnd()

    # Вызов обновления изображения

    def redraw(self):
        self.gl_widget.update()
