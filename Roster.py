import json
import Unit


class Roster:
    def __init__(self):
        self.roster_name = ""
        self.roster_faction = ""
        self.roster_owner = ""
        self.roster_power = 0
        self.roster_battles_total = 0
        self.roster_battles_won = 0
        self.roster_req_points = 0
        self.roster_supply_limit = 0
        self.roster_supply_used = 0
        # unit_list is a list of Unit objects, as defined above.
        self.unit_list = []
        # General crusade text for the roster, written and saved by the user
        self.roster_notes = ""
        # Contents of crusade_data will vary wildly from faction to faction,
        # as rules for Crusade mode are different for each faction in the game. 
        self.crusade_data = {}

    # Takes string 'unit_name_to_find' and sees if a unit with a matching name exists
    # Returns a boolean true/false
    def findUnit(self, unit_name_to_find):
        named_unit_exists = False
        for current in self.unit_list:
            if unit_name_to_find == current["name"]:
                named_unit_exists = True
                break
        return named_unit_exists

    # load a roster's data from JSON input
    def loadRosterFromJSON(self, JSON_to_load):
        self.roster_name = JSON_to_load["roster_name"]
        self.roster_faction = JSON_to_load["roster_faction"]
        self.roster_owner = JSON_to_load["roster_owner"]
        self.roster_power = JSON_to_load["roster_power"]
        self.roster_battles_total = JSON_to_load["roster_battles_total"]
        self.roster_battles_won = JSON_to_load["roster_battles_won"]
        self.roster_req_points = JSON_to_load["roster_req_points"]
        self.roster_supply_limit = JSON_to_load["roster_supply_limit"]
        self.roster_supply_used = JSON_to_load["roster_supply_used"]
        for entry in JSON_to_load["unit_list"]:
            temp_unit = Unit()
            temp_unit.loadFromDict(entry)
            self.unit_list.append(temp_unit)
        self.roster_notes = JSON_to_load["roster_notes"]
        self.crusade_data = JSON_to_load["crusade_data"]

    # Convert a roster to Dict format and return it
    # The method in main.py will call this during 
    # the Json serialization
    def outputRosterDict(self):
        JSON_to_output = {}
        JSON_to_output["roster_name"] = self.roster_name
        JSON_to_output["roster_faction"] = self.roster_faction
        JSON_to_output["roster_owner"] = self.roster_owner
        JSON_to_output["roster_power"] = self.roster_power
        JSON_to_output["roster_battles_total"] = self.roster_battles_total
        JSON_to_output["roster_battles_won"] = self.roster_battles_won
        JSON_to_output["roster_req_points"] = self.roster_req_points
        JSON_to_output["roster_supply_limit"] = self.roster_supply_limit
        JSON_to_output["roster_supply_used"] = self.roster_supply_used
        # Make an empty list, to be immediately filled with units
        JSON_to_output["unit_list"] = []
        for entry in self.unit_list:
            temp_unit_JSON = {}
            temp_unit_JSON = entry.convertToDict()
            JSON_to_output["unit_list"].append(temp_unit_JSON)
        JSON_to_output["roster_notes"] = self.roster_notes
        JSON_to_output["crusade_data"] = self.crusade_data
        return JSON_to_output

    # Add a new unit to the roster who's id number matches
    # the provided one.
    def addNewUnit(self, unit_id):
        unit_to_add = Unit()
        unit_to_add.loadUnitSQLData(unit_id)
        self.unit_list.append(unit_to_add)

    # Add an existing Unit object to unit_list
    def addExistingUnit(self, unit_to_add):
        if self.findUnit(unit_to_add["name"]) == False:
            self.unit_list.append(unit_to_add)
            self.roster_power += unit_to_add["power_level"]
        else:
            print("ERROR: Unit with that name already exists.")
    
    # Remove unit with the specified name from the list
    # 'unit_to_remove' should be a string
    def removeUnit(self, unit_to_remove):
        if self.findUnit(unit_to_remove) == True:
            # Lower power level of roster
            self.roster_power -= unit_to_remove["power_level"]
            # Remove unit from roster list
            for x in self.unit_list:
                if x["unit_title"] == unit_to_remove:
                    self.unit_list.remove(x)

# END of 'Roster' definition