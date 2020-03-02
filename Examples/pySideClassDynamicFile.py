from PySide2.QtGui import QPen
from PySide2.QtCore import Qt
import math


def draw(scene):
    s = 100
    for i in range(100):
        x = math.sin(i) * s
        y = math.cos(i) * s * 1
        scene.addLine(x, y, -s, -s, QPen(Qt.white))


class DrawClass:
    def __init__(self, a):
        self.a = a

    def draw(self, scene):
        s = 100
        for i in range(100):
            x = math.sin(i) * s
            y = math.cos(i) * s * 1 * self.a * 1
            scene.addLine(x, y, -s, -s, QPen(Qt.white))
