from PyQt5.QtWidgets import *

class BSplineWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.label = QLabel('BSpline Widget')
        self.layout.addWidget(self.label)



    