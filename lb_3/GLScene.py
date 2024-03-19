import numpy as np
from OpenGL.GL import *
from PyQt5.QtOpenGL import QGLWidget

from drawing import buildNurbs


class GLScene(QGLWidget):
    def __init__(self, parent=None):
        super(GLScene, self).__init__(parent)
        self.x = 0
        self.y = 0
        self.width = 600
        self.height = 800

    # Опорные точки
        self.P = [
            np.array([-0.9, -0.9]),
            np.array([-0.700, -0.3]),
            np.array([0.5, -0.4]),
            np.array([-0.200, -0.7]),
            np.array([0.9, 0.9])
        ]

        # Задаём узловой вектор
        self.T = np.arange(len(self.P) + 4)

        self.W = [1, 10, 100, 1000, 1]

        self.F, N = buildNurbs(self.T, self.P, self.W)

    def initializeGL(self):
        glClearColor(255.0, 255.0, 255.0, 1.0)
        glPointSize(10.0)
        glLineWidth(5.0)


        # glPointSize(5.0)
        # glLineWidth(3.0)

    def resizeGL(self, width, height):

        glViewport(0, 0, width, height)
        # self.viewPortResized.emit(width, height)

        # glMatrixMode(GL_PROJECTION)
        # glLoadIdentity()
        # aspect_ratio = width / height
        # if width <= height:
        #     glOrtho(-1.0, 1.0, -1.0 / aspect_ratio, 1.0 / aspect_ratio, -1.0, 1.0)
        # else:
        #     glOrtho(-1.0 * aspect_ratio, 1.0 * aspect_ratio, -1.0, 1.0, -1.0, 1.0)
        # glMatrixMode(GL_MODELVIEW)
        # glLoadIdentity()

    def paintGL(self):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glBegin(GL_POINTS)
        glColor3dv((1, 0, 0))
        for p in self.P:
            glVertex2dv(p)
        glEnd()

        glBegin(GL_LINE_STRIP)
        glColor3dv((0, 1, 0))
        for p in self.P:
            glVertex2dv(p)
        glEnd()

        glBegin(GL_LINE_STRIP)
        glColor3dv((0, 0, 0))
        X = np.linspace(1, 7, 1000)
        Points = [self.F(x) for x in X]
        for p in Points:
            glVertex2dv(p)
        glEnd()













