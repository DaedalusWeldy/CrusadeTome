# File for defining functions related to the UI,
# such as animations and page changes.

# Inspiration and ideas copied from video by
# Youtube video "Toggle Menu/Burguer Menu Animated"
# by Wanderson

# TEST: Will add specific QtCore sub-libraries once 
# I figure out which one it needs.

from main import *

class UIFunctions(MainWindow):
    def toggleMainMenu(self, max_width, is_enabled):
        if is_enabled:
            current_width = self.ui.left_menu_container.width()
            max_extend = max_width
            standard = 30

            if current_width == 30:
                extended_width = max_extend
            else:
                extended_width = standard
            
            #Animation controls
            self.animation = QPropertyAnimation(self.ui.left_menu_container, b"minimumWidth")
            self.animation.setDuration(400)
            self.animation.setStartValue(current_width)
            self.animation.setEndValue(extended_width)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()
