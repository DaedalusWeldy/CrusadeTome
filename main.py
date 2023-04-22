import sys
import platform
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QCoreApplication, QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import *

from RosterWindowV2 import Ui_MainWindow

# from UIFunctions import *

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.main_menu_button.clicked.connect(self.toggleMainMenu)

        self.show()

    def toggleMainMenu(self):
        # No matter the window size, don't want the menu to extend
        # Beyond size 150 or smaller than 25.
        MAX_WIDTH = 125 
        MIN_WIDTH = 40
        current_width = self.ui.left_menu_container.width()

        if current_width == MAX_WIDTH:
            desired_width = MIN_WIDTH
            self.ui.main_menu_button.setText("")
            self.ui.new_roster_button.setText("")
            self.ui.load_roster_button.setText("")
            self.ui.save_roster_button.setText("")
            self.ui.quit_button.setText("")
        elif current_width >= MIN_WIDTH:
            desired_width = MAX_WIDTH
            self.ui.main_menu_button.setText("Menu")
            self.ui.new_roster_button.setText("New Roster")
            self.ui.load_roster_button.setText("Load Roster")
            self.ui.save_roster_button.setText("Save Roster")
            self.ui.quit_button.setText("Quit Program")

            #Animation controls
        self.animation = QPropertyAnimation(self.ui.left_menu_container, b"minimumWidth")
        self.animation.setDuration(400)
        self.animation.setStartValue(current_width)
        self.animation.setEndValue(desired_width)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()


# Code responsible for actually launching the GUI.
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())