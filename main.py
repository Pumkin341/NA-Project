import sys
from PyQt5.QtWidgets import QApplication
from gui.mainFrame import MainFrame   

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainFrame()
    main_window.show()
    sys.exit(app.exec_())