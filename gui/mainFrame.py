from PyQt5.QtWidgets import *
from . import bezierWidget
from . import bsplineWidget

class MainFrame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Frame')
        self.setGeometry(100, 100, 1400, 850)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.button_layout = QHBoxLayout() 

        self.button1 = QPushButton('B-Spline')
        self.button2 = QPushButton('Bezier-de Casteljau')

        self.button_layout.addWidget(self.button1) 
        self.button_layout.addWidget(self.button2)

        self.layout.addLayout(self.button_layout) 

        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        self.bspline_widget = bsplineWidget.BSplineWidget()
        self.bezier_widget = bezierWidget.BezierWidget()

        self.stacked_widget.addWidget(self.bspline_widget)
        self.stacked_widget.addWidget(self.bezier_widget)

        self.button1.clicked.connect(self.show_bspline_widget)
        self.button2.clicked.connect(self.show_bezier_widget)

    def show_bspline_widget(self):
        self.stacked_widget.setCurrentWidget(self.bspline_widget)

    def show_bezier_widget(self):
        self.stacked_widget.setCurrentWidget(self.bezier_widget)