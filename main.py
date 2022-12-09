# CrusadeTome, a Warhammer 40k crusade mode data tracker
# Designed and coded by Daniel Weldy
# With data generously compiled by Wahapedia.ru. Thnak you! 

# Importing all QWidgets contents may not be the most efficient,
# But until I have a list of what widgets I need, it's easier 
# for testing purposes
import UnitAndRoster
from PyQt6 import QWidgets, uic
import json

# Class to define the main window of the program
# structure copied from nitratine.net tutorial, and edited for
# use in CrusadeTome.
class MainUI(QWidgets.QMainWindow):
    def __init__(self):
        super(MainUI.self).__init__()
        uic.load_ui('RosterListGUI.ui', self)
        self.show()
        # Global declaration doesn't work unless variable definition
        # and assignment are on separate lines
        global active_roster 
        active_roster = UnitAndRoster.Roster()

    def clearFields(self):
        # Clear all of the single-line fields
        self.force_name_line.clear()
        self.faction_line.clear()
        self.player_name_line.clear()
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
        self.force_name_line.text = active_roster.roster_name
        self.faction_line.text = active_roster.roster_faction
        self.player_name_line.text = active_roster.roster_owner
        self.battles_tally_line.text = active_roster.roster_battles_total
        self.battles_won_line.text = active_roster.roster_battles_won
        self.req_points.text = active_roster.roster_req_points
        self.supply_limit_line.text = active_roster.roster_supply_limit
        self.supply_used_line.text = active_roster.roster_supply_used
        # Change the number of rows to match the number of units
        # in the active roster's unit list.
        self.unit_list_table.setRowCount(len(active_roster.unit_list))
        # Load each unit in the unit list
        current_row = 0
        for entry in active_roster.unit_list:
            self.unit_list_table.setItem(current_row, 0, entry["name"])
            self.unit_list_table.setItem(current_row, 1, entry["power_level"])
            self.unit_list_table.setItem(current_row, 2, entry["crusade_points"])
            current_row += 1
        self.notes_text.text = active_roster.roster_notes
            

    # Load the roster data from a particular roster JSON
    # file and replace the current "active_roster" object. 
    # roster_file_path should be a string that represents the 
    # file path of the JSON file.
    def loadRosterFromJSONFile(self, roster_file_path):
        with open(roster_file_path, 'r') as file_input:
            data = file_input.read()
        temp_JSON = json.load(data)
        # Create a temporary 'Roster' object to populate with
        # data from the JSON
        active_roster.loadRosterFromJSON(temp_JSON)

    # Save current roster to a JSON file, for use later.
    def saveRosterToJSONFile(self):
        # Choose location via PyQt File Dialog window
        # Output roster as a JSON file
        