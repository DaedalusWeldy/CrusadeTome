import json
from operator import truediv
import sqlite3
import os
import re

# ************
# DEFINITIONS
# ************

# global variable to declare the file path of DB
# copied from https://help.pythonanywhere.com/pages/NoSuchFileOrDirectory/
THIS_FOLDER = os.path.dirname(__file__)
DB_PATH = os.path.join(THIS_FOLDER, r"WahapediaSQL.db")

# Strips extra HTML formatting from input_string, returns
# clean string of text
def stripHTML(input_string):
        return re.sub("<[^>]+>", '', input_string)

class Unit:
    def __init__(self):
        # Note that the unit will almost never be substantiated as a blank
        # unit for long; it will almost always immediately call the
        # 'loadUnitSQLData' method, or be loaded from an existing roster
        self.unit_title = "New Unit"
        self.name = "Unit Name"
        self.faction = "None"
        self.count = 0
        self.power_level = 0
        self.leader_name = "Unit Leader"
        self.role = "None"
        self.composition = "None"
        self.transport = "Not a transport"
        # chosen powers, such as SM litanies or Tau Etherial invocations
        self.chosen_power_text = "None"
        self.psychic_text = "Not a psychic"
        # Stats in modelList entries follow the same sequence that 
        # official Warhammer 40k datasheets use
        self.model_list = []
        self.wargear_list = []
        self.ability_list = []
        self.chosen_trait_list = []
        self.psychic_list = []
        self.keywords_list = []
        self.crusade_trait_list = []
        self.crusade_points = 0
        self.crusade_xp = 0
        self.battle_kills = {"ranged":0, "melee":0, "psychic":0}
        self.total_kills = {"ranged":0, "melee":0, "psychic":0}
        self.crusade_stats = {}

    # Returns boolean value based on whether or not unit has a
    # particular keyword
    def hasKeyword(self, keyword_to_find):
        has_keyword = False
        for entry in self.keywords_list:
            if (entry == keyword_to_find):
                has_keyword = True
        return has_keyword 

    # 'LoadUnitData' loads data for the chosen unit from WahapediaSQL.db
    # unit_to_load should be the string of the datasheet ID number
    def loadUnitSQLData(self, unit_to_load):
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            # Pulling raw info from Datasheets
            cursor = conn.execute("SELECT name, role, unit_composition, transport, priest, psyker, faction_id from Datasheets WHERE id=?", (unit_to_load,))
            result = cursor.fetchone()
            self.name = result["name"]
            self.role = result["role"]
            self.composition = stripHTML(result["unit_composition"])
            if self.transport != "":
                self.transport = result["transport"]
            if result["priest"] != "":
                self.priest_text = stripHTML(result['priest'])
            if result["psyker"] != "":
                self.psychic_text = result["psyker"]
            self.faction = result["faction_id"]
            print("Datasheets Data Loaded Successsfully")
            # Pulling ability pointer data
            cursor = conn.execute("SELECT line, ability_id, cost from Datasheets_abilities WHERE datasheet_id=?", (unit_to_load,))
            result = cursor.fetchall()
            for row in result:
                tempItem = {"ability_id": row["ability_id"], "cost":row["cost"]}
                self.ability_list.append(tempItem)
            # Using pointer data from previous step, pull actual text of abilities 
            for entry in self.ability_list:
                cursor = conn.execute("SELECT name, description from Abilities WHERE id=?", (entry["ability_id"],))
                result = cursor.fetchone()
                entry["name"] = result["name"]
                entry["description"] = stripHTML(result["description"])
            # Pulling in unit's associated keywords
            cursor = conn.execute("SELECT keyword, model from Datasheets_keywords WHERE datasheet_id=?", (unit_to_load,))
            result = cursor.fetchall()
            for row in result:
                if row["model"] != "":
                    self.keywords_list.append('' + row["keyword"] + '(' + row["model"] + ')')
                else:
                    self.keywords_list.append(row["keyword"])
            # Pulling stat values for each model in the unit
            cursor = conn.execute("SELECT name, M, WS, BS, S, T, W, A, Ld, Sv, Cost, cost_description," +
                "models_per_unit from Datasheets_models WHERE datasheet_id=?", (unit_to_load,))
            result = cursor.fetchall()
            for row in result:
                model_input = {"model_name": row["name"],
                    "model_M": row["M"], "model_WS": row["WS"],
                    "model_BS": row["BS"], "model_S": row["S"],
                    "model_T": row["T"], "model_W": row["W"],
                    "model_A": row["A"], "model_Ld": row["Ld"],
                    "model_Sv": row["Sv"], "model_count": 0}
                self.model_list.append(model_input)
            # Pulling list of wargear for the unit
            cursor = conn.execute("SELECT wargear_id, cost from Datasheets_wargear WHERE datasheet_id=?", (unit_to_load,))
            result =cursor.fetchall()
            for row in result:
                wargear_input = {"wargear_id": row["wargear_id"],
                                    "wargear_cost": row["cost"]}
                self.wargear_list.append(wargear_input)
            # Pulling data for each wargear piece
            for entry in self.wargear_list:
                cursor = conn.execute("SELECT name, type, description from Wargear WHERE id=?", (entry["wargear_id"],))
                cursor2 = conn.execute("SELECT name, range, type, S, AP, D, abilities from Wargear_list WHERE wargear_id=?", (entry["wargear_id"],))
                result = cursor.fetchone()
                result2 = cursor2.fetchall()
                entry["wargear_name"] = result["name"]
                entry["wargear_type"] = result["type"]
                entry["wargear_description"] = result["description"]
                # If result2 is only one entry, add descriptions to existing list item
                # Otherwise, add sub-gear below it on the list for each profile
                if len(result2) == 1:
                    entry["wargear_range"] = result2[0]["range"]
                    entry["wargear_type"] = result2[0]["type"]
                    entry["wargear_s"] = result2[0]["S"]
                    entry["wargear_ap"] = result2[0]["AP"]
                    entry["wargear_d"] = result2[0]["D"]
                    entry["wargear_abilities"] = stripHTML(result2[0]["abilities"])
                    entry["is_active"] = False
                elif len(result2) >= 2:
                    sub_entry = {"wargear_name":result2["name"], "wargear_type":result2["type"],
                                    "wargear_s":result2["S"], "wargear_ap":result2["AP"],
                                    "wargear_d":result2["d"], "wargear_abilities":result2["abilities"],
                                    "is_active": False}
                    self.wargear_list.insert(self.wargear_list.index(entry) + 1, sub_entry)
                else:
                    print("ERROR: Incorrect wargear generation!")
            # Pulling data for psyker abilities
            if self.psychic_text != "No psychic powers":
                cursor = conn.execute("SELECT roll, name, type, description from PsychicPowers WHERE type=?", (self.faction,))
                result =cursor.fetchall()
                for row in result:
                    psychic_power = {"power_name": row["name"], "power_roll": row["roll"],
                                    "power_type":row["type"], "power_description": stripHTML(row["description"]),
                                    "is_active": False}
                    self.psychic_list.append(psychic_power)
            # Pulling data for priest abilities, once a datasheet exists 
            # for them in the SQLite database.

            # Each set of crusade traits is associated with one or two keywords.
            # Find all lists for your faction that match this unit's keywords
            # and add them to the unit's 'crusade_trait_list'
            # Entries will be added as dictionaries
            """
            cursor = conn.execute("SELECT type, keyword1, keyword2, dice_num, trait_name, trait_text WHERE faction=?", (self.faction,))
            result = cursor.fetchall()
            for row in result:
                if self.hasKeyword(row["keyword1"]) and row["keyword2"] == "":
                    trait_to_add = {"name":row["trait_name"], "type":row["type"], 
                                    "text":row["trait_text"], "is_active":False}
                    self.crusade_trait_list.add(trait_to_add)
                elif self.hasKeyword(row["keyword1"]) and self.hasKeyword(row["keyword2"]):
                    trait_to_add = {"name":row["trait_name"], "type":row["type"], 
                                    "text":row["trait_text"], "is_active":False}
                    self.crusade_trait_list.add(trait_to_add)
            """        
                    


            # END of 'loadUnitSQLData' method
# END of 'Unit' definition

class Roster:
    def __init__(self):
        self.roster_name = "Roster name"
        self.roster_faction = "Faction"
        self.roster_owner = "Player name"
        self.roster_power = 0
        # unit_list is a list of Unit objects, as defined above.
        self.unit_list = []
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
        self.unit_list = JSON_to_load["unit_list"]
        self.crusade_data = JSON_to_load["crusade_data"]

    # Convert a roster to JSON format and return it
    def outputRosterJSON(self):
        JSON_to_output = json.dumps(self)
        return JSON_to_output

    # Add Unit object to unit_list
    def addUnit(self, unit_to_add):
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



# Testing section; to be cleared upon implementation of integrated testing 
print(DB_PATH)
testUnit = Unit()

testUnit.loadUnitSQLData("000002521")
print("The unit name is " + testUnit.name)
print("The unit role is " + testUnit.role)
print("The unit composition is " + testUnit.composition)
print("The unit transport is " + testUnit.transport)

for entry in testUnit.ability_list:
    print("Ability Name: " + entry['name'])
    print("Ability ID: " + entry['ability_id'])
    print("Ability Cost: " + entry['cost'])
    print("Ability Description: " + entry['description'])

for entry in testUnit.keywords_list:
    print(entry + ',')

for entry in testUnit.model_list:
    print(entry)

for entry in testUnit.psychic_list:
    print(entry)

for entry in testUnit.wargear_list:
    print(entry)
