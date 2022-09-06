import json
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

# Method does not work inside of class declaration
# but does work here
def stripHTML(input_string):
        return_text = re.sub("<[^>]+>", '', input_string)
        return return_text

class Unit:
    def __init__(self):
        self.name = "New Unit"
        self.faction = "None"
        self.count = 0
        self.leader_name = "Unit Leader"
        self.role = "None"
        self.composition = "None"
        self.transport = "Not a transport"
        self.priest_text = "Not a priest"
        self.psychic_text = "Not a psychic"
        # unitStats follows the same sequence that 
        # official Warhammer 40k datasheets use
        self.model_list = []
        self.wargear_list = []
        self.ability_list = []
        self.priest_list = []
        self.psychic_list = []
        self.keywords_list = []
        self.crusade_trait_list = []
        self.crusade_xp = []
        self.battle_kills = {"ranged":0, "melee":0, "psychic":0}
        self.total_kills = {"ranged":0, "melee":0, "psychic":0}

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
            # Pulling actual text of abilities 
            for entry in self.ability_list:
                cursor = conn.execute("SELECT name, description from Abilities WHERE id=?", (entry["ability_id"],))
                result = cursor.fetchone()
                entry["name"] = result["name"]
                entry["description"] = stripHTML(result["description"])
            # Pulling in unit keywords
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
                    "model_Sv": row["Sv"]}
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
                elif len(result2) >= 2:
                    sub_entry = {"wargear_name":result2["name"], "wargear_type":result2["type"],
                                    "wargear_s":result2["S"], "wargear_ap":result2["AP"],
                                    "wargear_d":result2["d"], "wargear_abilities":result2["abilities"]}
                    self.wargear_list.insert(self.wargear_list.index(entry) + 1, sub_entry)
                else:
                    print("ERROR: Incorrect wargear generation!")
            # Pulling data for psyker abilities
            if self.psychic_text != "No psychic powers":
                cursor = conn.execute("SELECT roll, name, type, description from PsychicPowers WHERE type=?", (self.faction,))
                result =cursor.fetchall()
                for row in result:
                    psychic_power = {"power_name": row["name"], "power_roll": row["roll"],
                                    "power_type":row["type"], "power_description": stripHTML(row["description"])}
                    self.psychic_list.append(psychic_power)
            # Pulling data for priest abilities, once a datasheet exists 
            # for them in the SQLite database.
    
    
    # 'SaveToJSON' Appends the Unit to the end of a JSON file
    # def saveToJSON(self, file_path):

    # 'LoadFromJSON' Appends the Unit to the end of a JSON file
    # def loadFromJSON(self, file_path):
# END of 'Unit' definition

# Testing section
print(DB_PATH)
testUnit = Unit()

testUnit.loadUnitSQLData("000000005")
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
