import sys
# import platform
import json
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableWidgetItem
from PyQt5.QtCore import QCoreApplication, QPropertyAnimation, QEasingCurve

# Importing roster and unit objects
from Roster import Roster
from Unit import Unit
from SQLFetcher import SQLFetcher

from RosterWindowV2 import Ui_MainWindow

# from UIFunctions import *

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.unit_loader = SQLFetcher()
        self.active_roster = Roster()
        self.available_units = []

        # Bind various functions to button clicks
        self.ui.main_menu_button.clicked.connect(self.toggleMainMenu)
        self.ui.add_unit_button.clicked.connect(self.showUnitSelectMenu)
        self.ui.close_add_unit_button.clicked.connect(self.hideUnitSelectMenu)
        self.ui.submit_unit_button.clicked.connect(self.addUnitToRoster)
        self.ui.load_roster_button.clicked.connect(self.loadRosterProcess)
        self.ui.save_roster_button.clicked.connect(self.saveRosterToJSONFile)
        self.ui.new_roster_button.clicked.connect(self.clearFields)

        # Change the list of available units whenever a selection in the
        # 'faction_select_combo' is made  
        self.ui.faction_select_combo.currentIndexChanged.connect(self.updateAvailableUnitList)

        # whenever any of the following line edits are changed on the Roster
        # page, update the 'active_roster' object with the new values
        self.ui.roster_name_line.editingFinished.connect(self.writeToRoster)
        self.ui.roster_faction_line.editingFinished.connect(self.writeToRoster)
        self.ui.roster_owner_line.editingFinished.connect(self.writeToRoster)
        self.ui.total_battles_line.editingFinished.connect(self.writeToRoster)
        self.ui.battles_won_line.editingFinished.connect(self.writeToRoster)
        self.ui.req_points_line.editingFinished.connect(self.writeToRoster)
        self.ui.supply_limit_line.editingFinished.connect(self.writeToRoster)
        self.ui.supply_used_line.editingFinished.connect(self.writeToRoster)
        # Though clunky, the TextEdit object only has a 'textChanged' signal
        self.ui.crusade_notes_text.textChanged.connect(self.writeToRoster)

        # Set menus to their starting postions
        self.hideUnitSelectMenu()

        # FUTURE PROJECT: Load unit data once, here (save r/w to/from database)
        self.updateFactionCombo()

        self.show()
# END of 'MainWindow' declaration


    # Please note: below this line are methods for use by the 
    # various UI elements.
    def clearFields(self):
        # Clear all of the single-line fields
        self.ui.roster_name_line.clear()
        self.ui.roster_faction_line.clear()
        self.ui.roster_owner_line.clear()
        self.ui.total_battles_line.clear()
        self.ui.battles_won_line.clear()
        self.ui.req_points_line.clear()
        self.ui.supply_limit_line.clear()
        self.ui.supply_used_line.clear()
        # Clear the contents of the table but keep the headers
        self.ui.unit_list_table.clearContents()
        self.ui.crusade_notes_text.clear()

    def writeToRoster(self):
        self.active_roster.roster_name = self.ui.roster_name_line.text()
        self.active_roster.roster_faction = self.ui.roster_faction_line.text()
        self.active_roster.roster_owner = self.ui.roster_owner_line.text()
        self.active_roster.roster_battles_total = self.ui.total_battles_line.text()
        self.active_roster.roster_battles_won = self.ui.battles_won_line.text()
        self.active_roster.roster_req_points = self.ui.req_points_line.text()
        self.active_roster.roster_supply_limit = self.ui.supply_limit_line.text()
        self.active_roster.roster_supply_used = self.ui.supply_used_line.text()
        self.active_roster.roster_notes = self.ui.crusade_notes_text.toPlainText()
        # No need to do units here; by nature of how the addUnit method works,
        # The unit list is updated with every unit added 
         

    def updateFields(self):
        self.ui.roster_name_line.setText(self.active_roster.roster_name)
        self.ui.roster_faction_line.setText(self.active_roster.roster_faction)
        self.ui.roster_owner_line.setText(self.active_roster.roster_owner)
        self.ui.total_battles_line.setText(str(self.active_roster.roster_battles_total))
        self.ui.battles_won_line.setText(str(self.active_roster.roster_battles_won))
        self.ui.req_points_line.setText(str(self.active_roster.roster_req_points))
        self.ui.supply_limit_line.setText(str(self.active_roster.roster_supply_limit))
        self.ui.supply_used_line.setText(str(self.active_roster.roster_supply_used))
        # Change the number of rows to match the number of units
        # in the active roster's unit list.
        self.ui.unit_list_table.clearContents()
        self.ui.unit_list_table.setRowCount(len(self.active_roster.unit_list))
        # Load each unit in the unit list
        current_row = 0
        for entry in self.active_roster.unit_list:
            # TO DO: Need to change last item in each getItem to a 'QTableWidgetItem' object
            self.ui.unit_list_table.setItem(current_row, 0, QTableWidgetItem(entry.name))
            self.ui.unit_list_table.setItem(current_row, 1, QTableWidgetItem(entry.power_level))
            self.ui.unit_list_table.setItem(current_row, 2, QTableWidgetItem(entry.crusade_points))
            current_row += 1
        self.ui.crusade_notes_text.setPlainText(self.active_roster.roster_notes)

    def toggleMainMenu(self):
        # No matter the window size, don't want the menu to extend
        # Beyond size 150 or smaller than 25.
        MAX_WIDTH = 125 
        MIN_WIDTH = 30
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
    # END of 'ToggleMainMenu' definition

    # hide and show have to be two separate functions, since they tie to
    # two separate buttons. 
    def hideUnitSelectMenu(self):
        self.ui.add_unit_container.hide()

    def showUnitSelectMenu(self):
        self.ui.add_unit_container.show()
        self.updateFactionCombo()

    def updateFactionCombo(self):
        for entry in self.unit_loader.fetchFactionList():
            faction_string = "" + entry["id"] + " - " + entry["name"]
            self.ui.faction_select_combo.addItem(faction_string)
        self.updateAvailableUnitList()

    # Update the list of available units with all of the units for
    # the selected faction 
    def updateAvailableUnitList(self):
        faction_id = ""
        current_selection = ""
        # Get the faction ID from the first two (or three) letters of 
        # the "faction_combo_box" text
        current_selection = self.ui.faction_select_combo.currentText()
        # TEST
        print(current_selection)
        if current_selection[2] == " ":
            faction_id = self.ui.faction_select_combo.currentText()[:2]
        else:
            faction_id = self.ui.faction_select_combo.currentText()[:3]
        # load the list of units using the fetchUnitList function of 
        # SQLFetcher
        self.available_units = self.unit_loader.fetchUnitList(faction_id)
        self.ui.unit_select_combo.clear()
        for entry in self.available_units:
            self.ui.unit_select_combo.addItem(str(entry.name))
        self.ui.unit_select_combo.setCurrentIndex(0)
    # END of 'updateAvailableUnitList' method

    def addUnitToRoster(self):
        # Takes the 'current_index' number from the currently selected 
        # comboBox item, then adds the Unit object from 'avaialble_units' 
        # with the same index number.
        unit_to_add = self.available_units[self.ui.unit_select_combo.currentIndex()]
        unit_to_add.crusade_points = 0
        self.active_roster.unit_list.append(unit_to_add)
        self.updateFields()

    # Load the roster data from a particular roster JSON
    # file and replace the current "active_roster" object. 
    # roster_file_path should be a string that represents the 
    # file path of the JSON file.
    def loadRosterFromJSONFile(self):
        # Set parameters for PyQt File Dialog window
        load_dialog = QFileDialog.getOpenFileName(self, "Select File...", "", "Roster files (*.ros);;All Files (*)")
        # If the dialog box opens, take the path that the user defines
        # and load the JSON data from the .ros file
        if load_dialog:
            filename = str(load_dialog[0])
            with open(filename, 'r') as file_input:
                # data = file_input.read()
                # Create a temporary 'Roster' object to populate with
                # data from the JSON
                temp_JSON = json.load(file_input)
                self.active_roster.loadRosterFromJSON(temp_JSON)
                self.clearFields()
                self.updateFields()

    # Save current roster to a JSON file, for use later.
    def saveRosterToJSONFile(self):
        self.writeToRoster()
        # Set parameters for PyQt File Dialog window
        save_dialog = QFileDialog.getSaveFileName(self, "Save File As...", "", "Roster files (*.ros);;All Files (*)")
        # If the dialog box opens, take the path that the user defines
        # And save a file to that location.
        if save_dialog[0] != "":
            filename = str(save_dialog[0])
            with open(filename, 'w') as file_output:
                temp_JSON = self.active_roster.outputRosterDict()
                json.dump(temp_JSON, file_output)
        # Testing to follow

    def loadRosterProcess(self):
        self.loadRosterFromJSONFile()
        self.clearFields()
        self.updateFields()

# Code responsible for actually launching the GUI.
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())