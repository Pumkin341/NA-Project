from PyQt5.QtWidgets import *

class BezierWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.label = QLabel('Bezier Widget')
        self.layout.addWidget(self.label)

        self.button = QPushButton('Button')
        self.layout.addWidget(self.button)




        