import json
import os
import sys
from Roster import Roster
from AddUnitDialog import AddUnitDialog
# from UnitStatsWindow import UnitStatsUI
# 'uic' is used for loading the .ui files from Qt Designer and
# converting them into usable classes
from PyQt6 import uic
# Import various Widget classes used by the Roster GUI
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (QApplication, QWidget, QTableWidgetItem, 
QMainWindow, QPushButton, QTableWidget, QLabel, QLineEdit, QTextEdit, 
QFileDialog)


# Class to define the main window of the program
# structure copied from nitratine.net tutorial, and edited for
# use in CrusadeTome.
class RosterWindow(QMainWindow):
    def __init__(self):
        super(RosterWindow, self).__init__()
        uic.loadUi(os.path.relpath("UI Templates/RosterListGUI.ui"), self)

        # Define all widgets using "findChild" method.
        # List of all QLabels
        self.force_name_label = self.findChild(QLabel, "force_name_label")
        self.faction_label = self.findChild(QLabel, "faction_label")
        self.player_name_label = self.findChild(QLabel, "player_name_label")
        self.battles_tally_label = self.findChild(QLabel, "battles_tally_label")
        self.battles_won_label = self.findChild(QLabel, "battles_won_label")
        self.req_point_label = self.findChild(QLabel, "req_point_label")
        self.supply_limit_label = self.findChild(QLabel, "supply_limit_label")
        self.supply_used_label = self.findChild(QLabel, "supply_used_label")
        self.crusade_goals_label = self.findChild(QLabel, "crusade_goals_label")
        # List of all QLineEdits
        self.force_name_line = self.findChild(QLineEdit, "force_name_line")
        self.faction_line = self.findChild(QLineEdit, "faction_line")
        self.player_line = self.findChild(QLineEdit, "player_line")
        self.battles_tally_line = self.findChild(QLineEdit, "battles_tally_line")
        self.battles_won_line = self.findChild(QLineEdit, "battles_won_line")
        self.req_points_line = self.findChild(QLineEdit, "req_points_line")
        self.supply_limit_line = self.findChild(QLineEdit, "supply_limit_line")
        self.supply_used_line = self.findChild(QLineEdit, "supply_used_line")
        # List of the table and the text box, for units and various
        # miscellaneous notes respectively
        self.unit_list_table = self.findChild(QTableWidget, "unit_list_table")
        self.notes_text = self.findChild(QTextEdit, "notes_text")
        # List of QPushButtons
        self.add_unit_button = self.findChild(QPushButton, "add_unit_button")
        self.remove_unit_button = self.findChild(QPushButton, "remove_unit_button")
        # List of QActions (The 'File' menu options)
        self.new_roster_action = self.findChild(QAction, "new_roster_action")
        self.save_roster_action = self.findChild(QAction, "save_roster_action")
        self.load_roster_action = self.findChild(QAction, "load_roster_action")

        # Assign actions to certain widgets
        self.new_roster_action.triggered.connect(self.clearFields)
        self.load_roster_action.triggered.connect(self.loadRosterProcess)
        self.save_roster_action.triggered.connect(self.saveRosterToJSONFile)
        self.add_unit_button.clicked.connect(self.addUnitProcess)

        self.active_roster = Roster()
        self.show()

    def clearFields(self):
        # Clear all of the single-line fields
        self.force_name_line.clear()
        self.faction_line.clear()
        self.player_line.clear()
        self.battles_tally_line.clear()
        self.battles_won_line.clear()
        self.req_points_line.clear()
        self.supply_limit_line.clear()
        self.supply_used_line.clear()
        # Clear the contents of the table but keep the headers
        self.unit_list_table.clearContents()
        self.notes_text.clear()

    # Update the values of the various UI fields to match
    # current values of the 'active_roster' object.
    def updateFields(self):
        self.force_name_line.text = self.active_roster.roster_name
        self.faction_line.text = self.active_roster.roster_faction
        self.player_line.text = self.active_roster.roster_owner
        self.battles_tally_line.text = self.active_roster.roster_battles_total
        self.battles_won_line.text = self.active_roster.roster_battles_won
        self.req_points_line.text = self.active_roster.roster_req_points
        self.supply_limit_line.text = self.active_roster.roster_supply_limit
        self.supply_used_line.text = self.active_roster.roster_supply_used
        # Change the number of rows to match the number of units
        # in the active roster's unit list.
        self.unit_list_table.clearContents()
        self.unit_list_table.setRowCount(len(self.active_roster.unit_list))
        # Load each unit in the unit list
        current_row = 0
        for entry in self.active_roster.unit_list:
            # TO DO: Need to change last item in each getItem to a 'QTableWidgetItem' object
            self.unit_list_table.setItem(current_row, 0, QTableWidgetItem(entry.name))
            self.unit_list_table.setItem(current_row, 1, QTableWidgetItem(entry.power_level))
            self.unit_list_table.setItem(current_row, 2, QTableWidgetItem(entry.crusade_points))
            current_row += 1
        self.notes_text.text = self.active_roster.roster_notes
            

    # Load the roster data from a particular roster JSON
    # file and replace the current "active_roster" object. 
    # roster_file_path should be a string that represents the 
    # file path of the JSON file.
    def loadRosterFromJSONFile(self, roster_file_path):
        # Set parameters for PyQt File Dialog window
        load_dialog = QFileDialog(self)
        load_dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        load_dialog.setNameFilter("CrusadeTome roster files (*.ros)")
        load_dialog.setDirectory("C:\\Users\%%current_user\\Documents")
        load_dialog.setDefaultSuffix("ros")
        load_dialog.setViewMode(QFileDialog.ViewMode.Detail)
        # If the dialog box opens, take the path that the user defines
        # and load the JSON data from the .ros file
        if load_dialog.exec():
            filename = load_dialog.selectedFiles()
            with open(filename, 'r') as file_input:
                data = file_input.read()
                # Create a temporary 'Roster' object to populate with
                # data from the JSON
                temp_JSON = json.loads(data)
                self.active_roster.loadRosterFromJSON(temp_JSON)

    # Save current roster to a JSON file, for use later.
    def saveRosterToJSONFile(self):
        # Set parameters for PyQt File Dialog window
        save_dialog = QFileDialog(self)
        save_dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        save_dialog.setNameFilter("CrusadeTome roster files (*.ros)")
        # TO DO change setDirectory to use pathlib
        save_dialog.setDirectory("C:\\Users\%%current_user\\Documents")
        save_dialog.setDefaultSuffix("ros")
        save_dialog.setViewMode(QFileDialog.ViewMode.Detail)
        # If the dialog box opens, take the path that the user defines
        # And save a .ros file to that location.
        if save_dialog.exec():
            filename = save_dialog.selectedFiles()
            with open(filename, 'w') as file_output:
                temp_JSON = self.active_roster.outputRosterDict()
                json.dumps(temp_JSON, file_output)
        # Testing to follow

    def loadRosterProcess(self):
        self.loadRosterFromJSONFile()
        self.clearFields()
        self.updateFields()

    # TO DO: Figure out why this opens two concurrent dialogs
    def addUnitProcess(self):
        add_unit_diag = AddUnitDialog()
        if add_unit_diag.exec():
            unit_to_add = add_unit_diag.available_units[add_unit_diag.unit_select_combo.currentIndex()]
            unit_to_add.crusade_points = 0
            # Takes the 'current_index' number from the currently selected unit, then 
            # adds the Unit object from 'avaialble_units' with the same index number.
            self.active_roster.unit_list.append(unit_to_add)
            # TEST
            unit_to_add.printUnit()
            self.updateFields()
        else:
            print("No unit added")

# END of 'MainUI' class

if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = RosterWindow()
    app.exec()