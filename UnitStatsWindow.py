from Unit import Unit
# 'uic' is used for loading the .ui files from Qt Designer and
# converting them into usable classes
from PyQt6 import uic
# Import various Widget classes used by the Roster GUI
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (QApplication, QWidget, 
QMainWindow, QPushButton, QTableView, QLabel, QLineEdit, QTextEdit, 
QFileDialog)
from pathlib import Path
import json
import sys

# Class to define the GUI for viewing Unit stats. To be opened whenever
# a user double-clicks on an entry in the unit list of the main roster
class UnitStatsWindow(QWidget):
    def __init__(self):
        super(UnitStatsWindow, self).__init__()
        uic.loadUi("\\UI Templates\\UnitStats.ui", self)

        # Add findChild for all of the widgets in the UnitStats UI 
        self.currentUnit = Unit()
        self.show()

    # Clear all fields in the window
    def clearFields(self):
        self.unit_name_line.clear()
        self.battlefield_role_line.clear()
        self.faction_line.clear()
        self.keywords_line.clear()
        self.unit_type_line.clear()
        self.equipment_line.clear()
        self.psychic_powers_line.clear()
        self.warlord_trait_line.clear()
        self.relic_line.clear()
        self.power_rating_line.clear()
        self.experience_points_line.clear()
        self.crusade_points_line.clear()
        self.selectable_traits_text.clear()

        self.battles_played_line.clear()
        self.battles_survived_line.clear()
        self.unit_rank_line.clear()
        self.enemy_unit_last_line.clear()
        self.enemy_unit_total_line.clear()
        self.enemy_psychic_last_line.clear()
        self.enemy_psychic_total_line.clear()
        self.enemy_ranged_last_line.clear()
        self.enemy_ranged_total_line.clear()
        self.enemy_melee_last_line.clear()
        self.enemy_melee_total_line.clear()
        self.agenda_one_last_line.clear()
        self.agenda_two_last_line.clear()
        self.agenda_three_last_line.clear()
        self.battle_honors_text.clear()
        self.battle_scars_text.clear()

        self.unit_stats_table.clear()
        self.wargear_table.clear()
        self.abilities_text.clear()

    # update all the fields in the window to reflect the current values
    # of currentUnit. 
    

    # loading values from the selected roster unit into 
    # currentUnit

    # Using current values from the window's fields, update currentUnit and
    # save it to the roster, overwriting the previous version of the unit

# END of "UnitStatsUI" definition