import sys
from PySide2.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QApplication,
    QFrame,
    QGraphicsView,
    QGraphicsScene,
)
from PySide2.QtCore import QTimer
from PySide2.QtCore import Qt
from PySide2.QtGui import QPainter, QColor, QBrush
from dynload import Dynload, safe_run
import pySideClassDynamicFile


class GraphicsViewer(QGraphicsView):
    def __init__(self, parent):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QBrush(QColor(30, 30, 30)))
        self.setFrameShape(QFrame.NoFrame)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

    def wheelEvent(self, event):
        adj = (event.delta() / 120) * 0.1
        self.scale(1 + adj, 1 + adj)


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.dynload = Dynload(pySideClassDynamicFile, qtimer=QTimer(self), callback=self.redraw)

        self.drawObj = pySideClassDynamicFile.DrawClass(5)

        self.setGeometry(150, 150, 1280, 720)
        self.viewer = GraphicsViewer(self)
        self.scene = self.viewer.scene
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.viewer)
        self.setLayout(self.layout)
        self.redraw()
        self.show()

    def redraw(self):
        self.scene.clear()

        # Example without save_run (could crash)
        # pySideDynamicFile.draw(self.scene)

        # Example with save_run so mistakes won't cause program crash
        safe_run(pySideClassDynamicFile.draw, self.scene)
        safe_run(self.drawObj.draw, self.scene)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
