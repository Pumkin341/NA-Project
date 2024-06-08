from PyQt5.QtWidgets import *
import bezierWidget
import bsplineWidget

class MainFrame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Frame')
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.button_layout = QHBoxLayout() 

        self.button1 = QPushButton('B-Spline')
        self.button2 = QPushButton('Bezier-de Casteljau')

        self.button_layout.addWidget(self.button1) 
        self.button_layout.addWidget(self.button2)

        self.layout.addLayout(self.button_layout) 
        self.widget = QWidget()
        self.layout.addWidget(self.widget)

        self.button1.clicked.connect(self.show_bezier_widget)
        self.button2.clicked.connect(self.show_bspline_widget)

    def show_bezier_widget(self):
        self.widget.deleteLater()
        self.widget = bsplineWidget.BSplineWidget()
        self.layout.addWidget(self.widget)

    def show_bspline_widget(self):
        self.widget.deleteLater()
        self.widget = bezierWidget.BezierWidget()
        self.layout.addWidget(self.widget)


if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')

    window = MainFrame()
    window.show()
    app.exec_()
