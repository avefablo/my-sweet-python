from sys import argv, exit

from PyQt4 import QtGui, QtCore


class Drawer(QtGui.QGraphicsView):
    def __init__(self, bmp_file):
        super(Drawer, self).__init__()
        self.scene = QtGui.QGraphicsScene()
        self.setScene(self.scene)
        self.filename = bmp_file.filename
        self.work = bmp_file.pixels
        self.is_reversed = bmp_file.is_reversed
        self.pic_width = len(self.work[0])
        self.pic_height = len(self.work)
        self.init_UI()
        self.draw_picture()

    def init_UI(self):
        """Инициализирует графический интерфейс"""
        self.resize(self.pic_width + 20, self.pic_height + 20)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setWindowTitle(self.filename)
        self.show()

    def draw_picture(self):
        """Рисует картинку попиксельно"""
        pix = QtGui.QPixmap(QtCore.QSize(self.pic_width, self.pic_height))
        qp = QtGui.QPainter(pix)
        x = 0
        y = len(self.work) - 1
        dy = -1
        if self.is_reversed:
            y = 0
            dy = 1
        for row in self.work:
            for element in row:
                color = QtGui.QColor(element.red, element.green,
                                     element.blue, element.alpha)
                qp.setPen(color)
                qp.drawPoint(x, y)
                x += 1
            y += dy
            x = 0
        self.scene.addPixmap(pix)
        qp.end()


def main(bmp_file):
    app = QtGui.QApplication(argv)
    ex = Drawer(bmp_file)
    app.exec_()
    app.deleteLater()
    exit()
