from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation

import numpy as np
from scipy import interpolate

import json, re

class BsplineFigure(FigureCanvas):
    def __init__(self, widget, width=5, height=5, dpi=100):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.grid()
        self.ax.set_title('B-Spline Curve')
        super().__init__(self.fig)
        self.widget = widget  
    
class AnimationWindow(QWidget):
    def __init__(self, points, degree, knots):
        super().__init__()
        self.points = points
        self.degree = degree
        self.knots = knots
        self.initUI()

    def initUI(self):
        self.setWindowTitle('B-Spline Animation')
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.figure = BsplineFigure(self)
        self.layout.addWidget(self.figure)

        self.startAnimation()

    def startAnimation(self):
        self.ax = self.figure.ax
        self.ax.clear()
        self.ax.grid()
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_title('B-Spline Curve Animation')
        
        ctr = np.array(self.points)
        x = ctr[:, 0]
        y = ctr[:, 1]

        tck = [self.knots, [x, y], self.degree]

        u3 = np.linspace(self.knots[self.degree], self.knots[-self.degree-1], 100, endpoint=True)
        self.out = interpolate.splev(u3, tck)

        self.line, = self.ax.plot([], [], 'b', label='B-spline curve')
        self.ax.plot(x, y, 'k--', label='Control polygon', marker='o', markerfacecolor='red')
        self.ax.legend(loc='best')

        self.anim = FuncAnimation(self.figure.fig, self.animate, init_func=self.init_anim, frames=100, interval=20, blit=True)

    def init_anim(self):
        self.line.set_data([], [])
        return self.line,

    def animate(self, i):
        self.line.set_data(self.out[0][:i], self.out[1][:i])
        return self.line,


class QHSeparationLine(QFrame):
    '''
    a horizontal separation line\n
    '''
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(1)
        self.setFixedHeight(20)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        return

class BSplineWidget(QWidget):
    
    pointsArray = []
    points = []
    lenght = 0
    degree = 0
    show_knots = 0
    
    def __init__(self):
        super().__init__()
        
        self.figure = BsplineFigure(self)
        
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        
        # figure 
        self.layout.addWidget(self.figure)
        self.separator = QHSeparationLine()
        
        # layouts
        self.bellowLayout = QHBoxLayout()
        self.leftLayout = QVBoxLayout()
        self.rightLayout = QGridLayout()
        self.bottomLayout = QHBoxLayout()
        
        # left
        self.addButton = QPushButton('Add Point')
        self.addButton.clicked.connect(self.add_point)
        self.leftLayout.addWidget(self.addButton)
        
        self.clearButton = QPushButton('Clear Points')
        self.clearButton.clicked.connect(self.clear_points)
        self.leftLayout.addWidget(self.clearButton)
        
        self.bellowLayout.addLayout(self.leftLayout)
        
        #right 
        self.degreeLabel = QLabel('Degree')
        self.degreeField = QLineEdit()
        reg_ex = QRegExp("[0-9]*")
        input_validator = QRegExpValidator(reg_ex)
        self.degreeField.setValidator(input_validator)
        
        self.degreeField.setText('3')
        self.rightLayout.addWidget(self.degreeLabel, 0, 0)
        self.rightLayout.addWidget(self.degreeField, 0, 1)
        
        self.knowVectorLabel = QLabel('Knot Vector')
        self.knotVectorField = QLineEdit()
        self.rightLayout.addWidget(self.knowVectorLabel, 1, 0)
        self.rightLayout.addWidget(self.knotVectorField, 1, 1)
        
        self.generateKnotsButton = QPushButton('Generate Knots')
        self.rightLayout.addWidget(self.generateKnotsButton, 2, 1)
        self.generateKnotsButton.clicked.connect(self.generate_knots)
        
        self.showKnots = QCheckBox('Show Knots')
        self.rightLayout.addWidget(self.showKnots, 2, 0)
        
        self.bellowLayout.addLayout(self.rightLayout)
        
        #bottom
        self.randomButton = QPushButton('Random Data')
        self.txtButton = QPushButton('Text Data')
        self.jsonButton = QPushButton('JSON Data')
        
        self.randomButton.clicked.connect(self.random_data)
        self.txtButton.clicked.connect(self.get_txt_data)
        self.jsonButton.clicked.connect(self.get_json_data)
        
        self.bottomLayout.addWidget(self.randomButton)
        self.bottomLayout.addWidget(self.txtButton)
        self.bottomLayout.addWidget(self.jsonButton)
        
        # Plot button
        self.PlotButton = QPushButton('Plot B-Spline Curve')
        self.PlotButton.clicked.connect(self.draw_bspline)
        
        self.plotInterpolateButton = QPushButton('Interpolate B-Spline Curve')
        self.plotInterpolateButton.clicked.connect(self.draw_interpolate)
        
        self.animateButton = QPushButton('Animate B-Spline Curve')
        self.animateButton.clicked.connect(self.open_animation_window)  
        

        self.layout.addWidget(self.separator)
        self.layout.addLayout(self.bellowLayout)
        self.layout.addWidget(self.separator)
        self.layout.addWidget(self.PlotButton)
        self.layout.addWidget(self.plotInterpolateButton)
        self.layout.addWidget(self.animateButton)
        self.layout.addWidget(self.separator)
        self.layout.addLayout(self.bottomLayout)
        
        self.errorLabel = QLabel()
        self.layout.addWidget(self.errorLabel)
        self.errorLabel.setStyleSheet('color: red')
        self.errorLabel.setAlignment(Qt.AlignCenter)
        
    def update_values(self):
        self.points = self.get_points()
        self.degree = self.get_degree()
        self.show_knots = self.get_show_knots()
         
    def get_points(self):
        coefficients = []
        
        if len(self.pointsArray) == 0:
            self.errorLabel.setText('Error: No points added')
            self.errorLabel.show()
            return
        
            
        for pointLayout in self.pointsArray:
            x = pointLayout.itemAt(1).widget().text()
            y = pointLayout.itemAt(2).widget().text()
            
            if x == '' or y == '':
                self.errorLabel.setText('Error: Empty fields')
                self.errorLabel.show()
                return
            
            coefficients.append([float(x), float(y)])
        return coefficients
    
    def get_knot_vector(self):
        if self.knotVectorField.text() == '':
            self.errorLabel.setText('Error: Empty Knot Vector')
            self.errorLabel.show()
            return
        
        return list(map(float, self.knotVectorField.text().split()))
    
    def get_degree(self):
        if self.degreeField.text() == '':
            self.errorLabel.setText('Error: Empty Degree')
            self.errorLabel.show()
            return
        return int(self.degreeField.text())
    
    def get_show_knots(self):
        return self.showKnots.isChecked()
    
    def add_point(self):
        
        point_name = "Point" + str(len(self.pointsArray) + 1)
        
        pointLayout = QGridLayout()
        pointLabel = QLabel(point_name)
        xField = QLineEdit()
        yField = QLineEdit()
        
        reg_ex = QRegExp("[0-9]+.?[0-9]{,2}")
        input_validator = QRegExpValidator(reg_ex)
        xField.setValidator(input_validator)
        yField.setValidator(input_validator)
        
        pointLayout.addWidget(pointLabel, 0, 0)
        pointLayout.addWidget(xField, 0, 1)
        pointLayout.addWidget(yField, 0, 2)
   
        self.pointsArray.append(pointLayout)
        self.leftLayout.addLayout(pointLayout)

    def clear_points(self):
        for pointLayout in self.pointsArray:
            for i in reversed(range(pointLayout.count())):
                widget = pointLayout.itemAt(i).widget()
                pointLayout.removeWidget(widget)
                widget.deleteLater()
            pointLayout.deleteLater()
        if self.pointsArray != []:
            self.pointsArray.clear()
        
        if self.points != []:
            self.points.clear()
        
    def generate_knots(self):
        if len(self.pointsArray) == 0:
            self.errorLabel.setText('Error: No points added')
            self.errorLabel.show()
            return
        
        degree = self.get_degree()
        if degree == None:
            return
        
        l = len(self.pointsArray)
        t = np.linspace(0, 1, l - degree + 1, endpoint=True)
        zeros = [0] * (degree)
        t = np.append(zeros, t)
        
        ones = [1] * (degree)
        t = np.append(t, ones)                
        t = np.round(t, decimals=2)
        
        self.knotVectorField.setText(' '.join(map(str, t)))
        
    def draw_bspline(self):
        self.update_values()
        plist = self.points

        if plist is None:
            self.figure.ax.clear()
            return
        if len(plist) < 2:
            self.figure.ax.clear()
            self.errorLabel.setText('Error: Not enough points')
            self.errorLabel.show()
            return

        degree = self.degree
        if degree is None:
            return
        if degree < 0:
            self.errorLabel.setText('Error: Degree must be positive')
            self.errorLabel.show()
            return

        try: 
            ctr = np.array(plist)
            x = ctr[:, 0]
            y = ctr[:, 1]

            l = len(ctr)

            # knots
            if self.knotVectorField.text() != '':
                t = self.get_knot_vector()
                if len(t) != l + degree + 1:
                    self.errorLabel.setText('Error: Number of knots must be equal to number of control points + degree + 1')
                    self.errorLabel.show()
                    return
            else: 
                t = np.linspace(0, 1, l - degree + 1, endpoint=True)
                zeros = [0] * (degree)
                t = np.append(zeros, t)

                ones = [1] * (degree)
                t = np.append(t, ones)                
                t = np.round(t, decimals=2)

                self.knotVectorField.setText(' '.join(map(str, t)))

            # knots, coefficients, degree
            tck = [t, [x, y], degree]

            # evaluate B-spline
            u3 = np.linspace(t[degree], t[-degree-1], 100, endpoint=True)
            out = interpolate.splev(u3, tck)

            self.errorLabel.hide()

            self.figure.ax.clear()
            self.figure.ax.grid()
            self.figure.ax.set_xlabel('x')
            self.figure.ax.set_ylabel('y')
            self.figure.ax.set_title('B-Spline Curve')
            
            self.figure.ax.plot(x, y, 'k--', label='Control polygon', marker='o', markerfacecolor='red')
            self.figure.ax.plot(out[0], out[1], 'b', label='B-spline curve')

            if self.show_knots:
                knots_x, knots_y = interpolate.splev(t[degree:-degree], tck)
                self.figure.ax.plot(knots_x, knots_y, 'go', label='Knots')

            self.figure.ax.legend(loc='best')
            self.figure.draw()

        except Exception as e:
            self.errorLabel.setText('Error: ' + str(e))
            self.errorLabel.show()
            return
    
    def draw_interpolate(self):
        
        self.update_values()
        plist = self.points
        
        if plist is None:
            self.figure.ax.clear()
            return
        if len(plist) < 2:
            self.figure.ax.clear()
            self.errorLabel.setText('Error: Not enough points')
            self.errorLabel.show()
            return
        
        degree = self.degree
        if degree is None:
            return
        if degree < 0:
            self.errorLabel.setText('Error: Degree must be positive')
            self.errorLabel.show()
            return
        
        try:
            ctr = np.array(plist)
            x = ctr[:, 0]
            y = ctr[:, 1]
            
            tck, u = interpolate.splprep([x, y], k=degree, s=0)
            u = np.linspace(0, 1, num=50, endpoint=True)
            out = interpolate.splev(u, tck)

            self.errorLabel.hide()

            self.figure.ax.clear()
            self.figure.ax.set_xlabel('x')
            self.figure.ax.set_ylabel('y')
            self.figure.ax.grid()
            self.figure.ax.set_title('Interpolated B-Spline Curve')
            
            self.figure.ax.plot(x, y, 'ro', label='Control points')
            self.figure.ax.plot(out[0], out[1], 'b', label='Interpolated B-spline')

            self.figure.ax.legend(loc='best')
            self.figure.draw()

        except Exception as e:
            self.errorLabel.setText('Error: ' + str(e))
            self.errorLabel.show()
            return
            
    def open_animation_window(self):
        self.update_values()
        
        if self.points is None or self.degree is None or self.points == [] or len(self.points) < 2:
            self.errorLabel.setText('Error: Not enough points')
            return
        
        knots = self.get_knot_vector()
        if knots is None:
            self.errorLabel.setText('Error: Empty Knot Vector')
            return
        
        if len(knots) != len(self.points) + self.degree + 1:
            self.errorLabel.setText('Error: Number of knots must be equal to number of control points + degree + 1')
            return
        
        self.errorLabel.hide()
    
        self.anim_window = AnimationWindow(self.points, self.degree, knots)
        self.anim_window.show()
        
    def random_data(self):
        self.figure.ax.clear()
        
        n = np.random.randint(2, 10)
        if self.pointsArray:
            self.clear_points()
        for i in range(n):
            self.add_point()
            x = np.random.randint(0, 10)
            y = np.random.randint(0, 10)
            pointLayout = self.pointsArray[-1]
            xField = pointLayout.itemAt(1).widget()
            yField = pointLayout.itemAt(2).widget()
            xField.setText(str(x))
            yField.setText(str(y))
            
        degree = np.random.randint(1, len(self.pointsArray))
        self.degreeField.setText(str(degree))
        
        self.generate_knots()
    
    def get_txt_data(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '', 'Text Files (*.txt)')[0]
        if filename == '':
            return
        
        with open(filename, 'r') as file:
            lines = file.readlines()

            self.figure.ax.clear()
            points_line = lines[0].strip()
            points = []
            points_str = points_line[1:-1].replace('), (', '),(').split('),(')

            for point_str in points_str:
                point = point_str.split(',')
                points.append((float(point[0]), float(point[1])))

            self.clear_points()
            for point in points:
                self.add_point()
                pointLayout = self.pointsArray[-1]
                xField = pointLayout.itemAt(1).widget()
                yField = pointLayout.itemAt(2).widget()
                xField.setText(str(point[0]))
                yField.setText(str(point[1]))
            
            degree = int(lines[1].strip())
            self.degreeField.setText(str(degree))
            
            self.knotVectorField.setText('')
            if len(lines) > 2:
                knots = []
                knots_line = lines[2].strip()
                knots = list(map(float, knots_line.split()))
                self.knotVectorField.setText(' '.join(map(str, knots)))
        
    def get_json_data(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '', 'JSON Files (*.json)')[0]
        if filename == '':
            return

        with open(filename, 'r') as file:
            json_data = json.load(file)

            if 'points' not in json_data or 'degree' not in json_data:
                self.errorLabel.setText('Error: JSON file does not contain points or degree')
                self.errorLabel.show()
                return

            self.figure.ax.clear()
            
            points_str = json_data['points']
            points = re.findall(r'\(([^)]+)\)', points_str)
            points = [tuple(map(float, point.split(','))) for point in points]

            if self.pointsArray:
                self.clear_points()
                
            for point in points:
                self.add_point()
                pointLayout = self.pointsArray[-1]
                xField = pointLayout.itemAt(1).widget()
                yField = pointLayout.itemAt(2).widget()
                xField.setText(str(point[0]))
                yField.setText(str(point[1]))

            degree = json_data['degree']
            self.degreeField.setText(str(degree))

            self.knotVectorField.setText('')
            if 'knots' in json_data and json_data['knots'] != 'None':
                knots_str = json_data['knots']
                knots = list(map(float, knots_str.split()))
                self.knotVectorField.setText(' '.join(map(str, knots)))

                