import math
import random
import sys

from OpenGL.GL import *
from PyQt5.QtCore import Qt
from PyQt5.QtOpenGL import QGLWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QLabel, QHBoxLayout, QSlider


class GLScene(QGLWidget):
    def __init__(self, parent=None):
        super(GLScene, self).__init__(parent)
        self.primitiveMode = GL_POINTS
        self.alpha = GL_ALWAYS
        self.alpha_value = 1.0
        self.sfactor = GL_ONE
        self.dfactor = GL_ONE
        self.x = 0
        self.y = 0
        self.width = 800
        self.height = 600

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
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

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        colors = [
            (0.0, 1.0, 1.0), (1.0, 0.0, 1.0), (0.0, 0.5, 0.0),
            (0.5, 0.0, 0.0), (0.0, 0.5, 0.5), (0.5, 0.0, 0.5),
            (0.0, 1.0, 0.0), (1.0, 0.0, 0.0), (1.0, 1.0, 0.0),
            (0.0, 0.0, 1.0)
        ]

        num_points = 12
        radius = 0.5

        glEnable(GL_ALPHA_TEST)
        glEnable(GL_BLEND)
        glEnable(GL_SCISSOR_TEST)
        glAlphaFunc(self.alpha, self.alpha_value)
        glBlendFunc(self.sfactor, self.dfactor)
        glScissor(self.x, self.height - self.y - self.height, self.width, self.height)
        glBegin(self.primitiveMode)
        for point in range(num_points):
            glColor4f(colors[point % len(colors)][0], colors[point % len(colors)][1], colors[point % len(colors)][2],
                      random.uniform(0.2, 1.0))
            angle = 2 * math.pi * point / num_points
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            glVertex2f(x, y)
        glEnd()


def generate_dictionary(words):
    return {word: globals()[word] for word in words if word in globals()}


def create_text(text, layout):
    title = QLabel(text)
    title.setMaximumHeight(15)
    layout.addWidget(title)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Чернякова Валерия, Ярусова Татьяна КГ Лаб. 1")
        self.setGeometry(100, 100, 800, 600)
        self.pickers = {}
        self.all_QComboBox = {}
        self.slider_labels = {}

        central_widget = QWidget()
        layout = QHBoxLayout()
        vertical_layout = QVBoxLayout()
        layout.addLayout(vertical_layout)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.gl_widget = GLScene()
        layout.addWidget(self.gl_widget)

        create_text("Лабораторная работа №1", vertical_layout)
        create_text("Примитивы OpenGL", vertical_layout)

        self.pickers['primitives'] = QComboBox()
        vertical_layout.addWidget(self.pickers['primitives'])
        self.primitives = ["GL_POINTS", "GL_LINES", "GL_LINE_STRIP", "GL_LINE_LOOP", "GL_TRIANGLES",
                           "GL_TRIANGLE_STRIP", "GL_TRIANGLE_FAN", "GL_QUADS", "GL_QUAD_STRIP", "GL_POLYGON"]
        self.all_QComboBox['primitives'] = generate_dictionary(self.primitives)
        self.init_QComboBox('primitives')

        create_text("Лабораторная работа №2", vertical_layout)
        create_text("Тест прозрачности", vertical_layout)

        self.pickers['alpha'] = QComboBox()
        vertical_layout.addWidget(self.pickers['alpha'])
        self.alpha = ["GL_ALWAYS", "GL_NEVER", "GL_LESS", "GL_EQUAL", "GL_LEQUAL", "GL_GREATER", "GL_NOTEQUAL",
                      "GL_GEQUAL"]
        self.all_QComboBox['alpha'] = generate_dictionary(self.alpha)
        self.init_QComboBox('alpha')

        self.create_slider(0, 100, 100, 'a', vertical_layout)

        create_text("Тест смешения цветов", vertical_layout)

        self.pickers['sfactor'] = QComboBox()
        vertical_layout.addWidget(self.pickers['sfactor'])
        self.sfactor = ["GL_ONE", "GL_ZERO", "GL_DST_COLOR", "GL_ONE_MINUS_DST_COLOR", "GL_SRC_ALPHA",
                        "GL_ONE_MINUS_SRC_ALPHA", "GL_DST_ALPHA", "GL_ONE_MINUS_DST_ALPHA", "GL_SRC_ALPHA_SATURATE"]
        self.all_QComboBox['sfactor'] = generate_dictionary(self.sfactor)
        self.init_QComboBox('sfactor')

        self.pickers['dfactor'] = QComboBox()
        vertical_layout.addWidget(self.pickers['dfactor'])
        self.dfactor = ["GL_ONE", "GL_ZERO", "GL_SRC_COLOR", "GL_ONE_MINUS_SRC_COLOR", "GL_SRC_ALPHA",
                        "GL_ONE_MINUS_SRC_ALPHA", "GL_DST_ALPHA", "GL_ONE_MINUS_DST_ALPHA"]
        self.all_QComboBox['dfactor'] = generate_dictionary(self.dfactor)
        self.init_QComboBox('dfactor')

        create_text("Тест отсечения", vertical_layout)

        create_text("x", vertical_layout)
        self.create_slider(0, 800, 0, 'x', vertical_layout)
        create_text("y", vertical_layout)
        self.create_slider(0, 600, 0, 'y', vertical_layout)
        create_text("Ширина", vertical_layout)
        self.create_slider(0, 600, 600, 'w', vertical_layout)
        create_text("Высота", vertical_layout)
        self.create_slider(0, 800, 800, 'h', vertical_layout)

    def init_QComboBox(self, box_type):
        self.pickers[box_type].addItems(self.all_QComboBox[box_type].keys())
        self.pickers[box_type].setCurrentText(next(iter(self.all_QComboBox[box_type].keys())))
        self.pickers[box_type].currentTextChanged.connect(self.on_picker_current_text_changed)

    def on_picker_current_text_changed(self, text):
        if text in self.primitives:
            self.gl_widget.primitiveMode = self.all_QComboBox['primitives'][text]
        elif text in self.alpha:
            self.gl_widget.alpha = self.all_QComboBox['alpha'][text]
        elif text in self.sfactor:
            self.gl_widget.sfactor = self.all_QComboBox['sfactor'][text]
        elif text in self.dfactor:
            self.gl_widget.dfactor = self.all_QComboBox['dfactor'][text]
        self.gl_widget.update()
        self.gl_widget.paintGL()

    def create_slider(self, min_value, max_value, start_value, slider_name, layout):
        slider = QSlider(Qt.Horizontal)
        slider.setFixedWidth(200)
        slider.setMinimum(min_value)
        slider.setMaximum(max_value)
        slider.setValue(start_value)
        slider.setTickInterval(10)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setObjectName(slider_name)
        slider.valueChanged.connect(self.on_slider_value_changed)
        layout.addWidget(slider)

        if slider_name == 'a':
            self.slider_labels[slider_name] = QLabel(f"Выбранное значение: {start_value / 100}", self)
        else:
            self.slider_labels[slider_name] = QLabel(f"Выбранное значение: {start_value}", self)
        layout.addWidget(self.slider_labels[slider_name])

    def on_slider_value_changed(self, value):
        sender = self.sender()
        slider_name = sender.objectName()
        if slider_name == 'x':
            self.slider_labels['x'].setText(f"Выбранное значение: {value}")
            self.gl_widget.x = value
        elif slider_name == 'y':
            self.slider_labels['y'].setText(f"Выбранное значение: {value}")
            self.gl_widget.y = value
        elif slider_name == 'w':
            self.slider_labels['w'].setText(f"Выбранное значение: {value}")
            self.gl_widget.width = value
        elif slider_name == 'h':
            self.slider_labels['h'].setText(f"Выбранное значение: {value}")
            self.gl_widget.height = value
        elif slider_name == 'a':
            self.slider_labels['a'].setText(f"Выбранное значение: {value / 100}")
            self.gl_widget.alpha_value = value / 100
        self.gl_widget.update()
        self.gl_widget.paintGL()


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
