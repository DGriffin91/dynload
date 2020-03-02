from PySide2.QtGui import QPen
from PySide2.QtCore import Qt
import math


def draw(scene):
    s = 100
    for i in range(100):
        x = math.sin(i) * s
        y = math.cos(i) * s * 2
        scene.addLine(x, y, -s, -s, QPen(Qt.white))
