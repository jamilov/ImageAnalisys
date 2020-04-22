import os
import PyQt5.QtGui
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from Calculations import *
import sys
(Ui_MainWindow, QMainWindow) = uic.loadUiType('dialog1.ui')


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Button actions
        self.ui.save.clicked.connect(saveImage)
        self.ui.browse.clicked.connect(self.initUI)
        self.ui.exit.clicked.connect(self.exitClicked)

        self.ui.average.clicked.connect(self.averageClicked)
        self.ui.firstblur.clicked.connect(self.firstblurClicked)
        self.ui.secondblur.clicked.connect(self.secondblurClicked)
        self.ui.enthropy.clicked.connect(self.enthropyClicked)
        self.ui.segmentation.clicked.connect(self.segmentationClicked)
        self.ui.sharpness.clicked.connect(self.sharpnessClicked)
        self.ui.sharpness2.clicked.connect(self.sharpness2Clicked)

        #Menu actions
        self.ui.action_2.triggered.connect(self.initUI)
        self.ui.action_5.triggered.connect(saveImage)
        self.ui.action_7.triggered.connect(self.exitClicked)
        self.ui.img.setPixmap(PyQt5.QtGui.QPixmap("hi.png"))

    def averageClicked(self):
        self.setImage(average())

    def firstblurClicked(self):
        message("Мера размытости изображения", str(firstblur()))

    def secondblurClicked(self):
        message("Мера размытости изображения", str(secondblur()))

    def enthropyClicked(self):
        message("Мера энтропии изображения", str(enthropy()))

    def segmentationClicked(self):
        message("Мера сегментации изображения", str(segmentation()))

    def sharpnessClicked(self):
        message("Мера резкости изображения", str(sharpness()))

    def sharpness2Clicked(self):
        message("Мера резкости изображения", str(sharpness2()))

    def exitClicked(self):
        QtCore.QCoreApplication.instance().quit()

    def setImage(self, image):
        self.ui.img.setPixmap(PyQt5.QtGui.QPixmap.fromImage(image))

    def getFileName(self):
        filename = self.ui.lineEdit.text()
        return filename

    def initUI(self):
        fileName = QFileDialog.getOpenFileName(self, "Open Image", "/Users/parviz_jamilov/Desktop/Анализ изображений", "Image Files (*.png *.jpg *.bmp)");
        self.ui.lineEdit.setText(str(fileName[0]))
        self.ui.img.setPixmap(PyQt5.QtGui.QPixmap(str(fileName[0])))
        filename = self.ui.lineEdit.text()
        if os.path.exists(filename):
            loadImage(filename)
        else:
            message("Ошибка сохранения", "Изображение не создано!")

    def __del__(self):
        self.ui = None


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
