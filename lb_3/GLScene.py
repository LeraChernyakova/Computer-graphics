import math
import random

from OpenGL.GL import *
from PyQt5.QtCore import QRectF, QSizeF, Qt, QPointF
from PyQt5.QtGui import QVector2D, QColor
from PyQt5.QtOpenGL import QGLWidget
from PyQt5.QtWidgets import QWidget


class GLScene(QGLWidget):
    def __init__(self, parent=None):
        super(GLScene, self).__init__(parent)
        self.x = 0
        self.y = 0
        self.width = 600
        self.height = 800

    def initializeGL(self):
        glClearColor(255.0, 255.0, 255.0, 1.0)
        glPointSize(5.0)
        glLineWidth(3.0)

    def resizeGL(self, width, height):

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect_ratio = width / height
        if width <= height:
            glOrtho(-1.0, 1.0, -1.0 / aspect_ratio, 1.0 / aspect_ratio, -1.0, 1.0)
        else:
            glOrtho(-1.0 * aspect_ratio, 1.0 * aspect_ratio, -1.0, 1.0, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def paintGL(self):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)







