from Unit import Unit
from SQLFetcher import SQLFetcher
# 'uic' is used for loading the .ui files from Qt Designer and
# converting them into usable classes
from PyQt6 import uic
# Import various Widget classes used by the Roster GUI
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (QDialog, QComboBox, QDialogButtonBox, QApplication)

import os
import sys

# Class to define the dialog window for adding a unit to the roster
class AddUnitDialog(QDialog):
    def __init__(self, parent=None):
        super(AddUnitDialog, self).__init__()
        uic.loadUi(os.path.relpath("UI Templates/AddUnitDialog.ui"), self)
        
        self.faction_select_combo = self.findChild(QComboBox, "faction_select_combo")
        self.unit_select_combo = self.findChild(QComboBox, "unit_select_combo")
        self.button_box = self.findChild(QDialogButtonBox, "button_box")

        self.faction_select_combo.currentIndexChanged.connect(self.updateAvailableUnitList)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.unit_loader = SQLFetcher()
        
        # List object of the available units from your faction
        self.updateFactionCombo()
        self.available_units = []
        # TEST self.exec()

    # TO DO
    # Fill out faction_select_combo with a list of all of the 
    # factions in the game.
    def updateFactionCombo(self):
        for entry in self.unit_loader.fetchFactionList():
            faction_string = "" + entry["id"] + " - " + entry["name"]
            self.faction_select_combo.addItem(faction_string)
        self.faction_select_combo.setCurrentIndex(0)

    # Update the list of available units with all of the units for
    # the selected faction 
    def updateAvailableUnitList(self):
        faction_id = ""
        current_selection = ""
        # Get the faction ID from the first two (or three) letters of 
        # the "faction_combo_box" text
        current_selection = self.faction_select_combo.currentText()
        # TEST
        print(current_selection)

        if current_selection[2] == " ":
            faction_id = self.faction_select_combo.currentText()[:2]
        else:
            faction_id = self.faction_select_combo.currentText()[:3]
        # load the list of units using the fetchUnitList function of 
        # SQLFetcher
        self.available_units = self.unit_loader.fetchUnitList(faction_id)
        self.unit_select_combo.clear()
        for entry in self.available_units:
            self.unit_select_combo.addItem(str(entry.name))
        self.unit_select_combo.setCurrentIndex(0)
        

    # TO DO
    # Method that will add the selected unit to the current Roster's 
    # 'unit_list' (from RosterWindow)
    # def addUnitAction(self):


# TO DO
# Add "__main__" clause to end of file for testing purposes
if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = AddUnitDialog()
    app.exec()