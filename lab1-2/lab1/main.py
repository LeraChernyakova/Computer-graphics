import math
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QLabel, QSlider
from PyQt5.QtOpenGL import QGLWidget
from OpenGL.GL import *


class GLScene(QGLWidget):
    def __init__(self, parent=None):
        super(GLScene, self).__init__(parent)
        self.primitiveMode = GL_POINTS
        self.transparency = GL_ALWAYS
        self.transparency_value = 1.0

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glPointSize(5.0)
        glLineWidth(3.0)
        glEnable(GL_ALPHA_TEST)

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

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        colors = [
            (0.0, 1.0, 1.0), (1.0, 0.0, 1.0), (0.0, 0.5, 0.0),
            (0.5, 0.0, 0.0), (0.0, 0.5, 0.5), (0.5, 0.0, 0.5),
            (0.0, 1.0, 0.0), (1.0, 0.0, 0.0), (1.0, 1.0, 0.0),
            (0.0, 0.0, 1.0)
        ]

        num_points = 10
        radius = 0.5
        center_x, center_y = 0.0, 0.0

        glAlphaFunc(self.transparency, self.transparency_value)
        glBegin(self.primitiveMode)
        for i in range(len(colors)):
            glColor3f(colors[i][0], colors[i][1], colors[i][2])
            angle = 2 * math.pi * i / num_points
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            glVertex2f(x, y)
        glEnd()
        glDisable(GL_ALPHA_TEST)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Чернякова Валерия, Ярусова Татьяна КГ Лаб. 1")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.gl_widget = GLScene()
        layout.addWidget(self.gl_widget)

        lab_title = QLabel("Лабораторная работа №1")
        lab_title.setMaximumHeight(20)
        layout.addWidget(lab_title)

        self.primitive_picker = QComboBox()
        layout.addWidget(self.primitive_picker)

        self.setCentralWidget(central_widget)

        self.primitive_types = {
            "GL_POINTS": GL_POINTS,
            "GL_LINES": GL_LINES,
            "GL_LINE_STRIP": GL_LINE_STRIP,
            "GL_LINE_LOOP": GL_LINE_LOOP,
            "GL_TRIANGLES": GL_TRIANGLES,
            "GL_TRIANGLE_STRIP": GL_TRIANGLE_STRIP,
            "GL_TRIANGLE_FAN": GL_TRIANGLE_FAN,
            "GL_QUADS": GL_QUADS,
            "GL_QUAD_STRIP": GL_QUAD_STRIP,
            "GL_POLYGON": GL_POLYGON
        }

        self.init_primitives()

        lab_title = QLabel("Лабораторная работа №2")
        lab_title.setMaximumHeight(20)
        layout.addWidget(lab_title)

        lab_title = QLabel("Тест прозрачности")
        lab_title.setMaximumHeight(20)
        layout.addWidget(lab_title)

        self.transparency_picker = QComboBox()
        layout.addWidget(self.transparency_picker)

        self.transparency_types = {
            "GL_ALWAYS": GL_ALWAYS,
            "GL_NEVER": GL_NEVER,
            "GL_LESS": GL_LESS,
            "GL_EQUAL": GL_EQUAL,
            "GL_LEQUAL": GL_LEQUAL,
            "GL_GREATER": GL_GREATER,
            "GL_NOTEQUAL": GL_NOTEQUAL,
            "GL_GEQUAL": GL_GEQUAL
        }

        self.init_transparency()

        self.slider = QSlider(Qt.Horizontal)  # Создание горизонтального ползунка
        self.slider.setMinimum(0)  # Минимальное значение
        self.slider.setMaximum(100)  # Максимальное значение
        self.slider.setValue(100)  # Начальное значение
        self.slider.setTickInterval(10)  # Интервал между делениями
        self.slider.setTickPosition(QSlider.TicksBelow)  # Позиция делений под ползунком

        self.slider.valueChanged.connect(self.on_slider_value_changed)  # Подключение слота к сигналу valueChanged

        layout.addWidget(self.slider)

        self.label = QLabel("Выбранное значение: 1", self)
        layout.addWidget(self.label)

        self.setCentralWidget(central_widget)

        lab_title = QLabel("Тест смешения цветов")
        lab_title.setMaximumHeight(20)
        layout.addWidget(lab_title)

        lab_title = QLabel("sfactor")
        lab_title.setMaximumHeight(20)
        layout.addWidget(lab_title)

        self.sfactor_picker = QComboBox()
        layout.addWidget(self.sfactor_picker)

        self.sfactor_types = {
            "GL_ZERO": GL_ALWAYS,
            "GL_ONE": GL_NEVER,
            "GL_DST_COLOR": GL_LESS,
            "GL_ONE_MINUS_DST_COLOR": GL_EQUAL,
            "GL_SRC_ALPHA": GL_LEQUAL,
            "GL_ONE_MINUS_SRC_ALPHA": GL_GREATER,
            "GL_DST_ALPHA": GL_NOTEQUAL,
            "GL_GEQUAL": GL_GEQUAL
        }

        self.init_transparency()

    def init_primitives(self):
        self.primitive_picker.addItems(self.primitive_types.keys())
        self.primitive_picker.setCurrentText("GL_POINTS")
        self.primitive_picker.currentTextChanged.connect(self.on_primitive_picker_current_text_changed)

    def on_primitive_picker_current_text_changed(self, text):
        self.gl_widget.primitiveMode = self.primitive_types[text]
        self.gl_widget.update()
        self.gl_widget.paintGL()

    def init_transparency(self):
        self.transparency_picker.addItems(self.transparency_types.keys())
        self.transparency_picker.setCurrentText("GL_ALWAYS")
        self.transparency_picker.currentTextChanged.connect(self.on_transparency_picker_current_text_changed)

    def on_transparency_picker_current_text_changed(self, text):
        self.gl_widget.transparency = self.transparency_types[text]
        self.gl_widget.update()
        self.gl_widget.paintGL()

    def on_slider_value_changed(self, value):
        self.label.setText(f"Выбранное значение: {value/100}")
        self.gl_widget.transparency_value = value
        self.gl_widget.update()
        self.gl_widget.paintGL()


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
