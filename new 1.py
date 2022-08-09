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
        self.stats = {"move":0,"weapon_skill":0,
                          "ballistic_skill":0,"strength":0,
                          "toughness":0,"wounds":0, "attacks":0,
                          "leadership":0,"save":0}
        self.leader_stats = {"move":0,"weapon_skill":0,
                          "ballistic_skill":0,"strength":0,
                          "toughness":0,"wounds":0,"attacks":0,
                          "leadership":0,"save":0}
        self.weapon_list = []
        self.ability_list = []
        self.priest_list = []
        self.psychic_list = []
        self.crusade_trait_list = []
        self.crusade_xp = []
        self.battle_kills = {"ranged":0, "melee":0, "psychic":0}
        self.total_kills = {"ranged":0, "melee":0, "psychic":0}

    # 'LoadUnitData' loads data for the chosen unit from WahapediaSQL.db
    # unit_to_load should be the string of the datasheet ID number
    def loadUnitSQLData(self, unit_to_load):
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT name, role, unit_composition, transport, priest, psyker, faction_id from Datasheets WHERE id=?", (unit_to_load,))
            result = cursor.fetchone()
            self.name = result['name']
            self.role = result['role']
            self.composition = stripHTML(result['unit_composition'])
            self.transport = result['transport']
            self.priest_text = result['priest']
            self.psychic_text = result['psyker']
            self.faction = result['faction_id']
            print("Datasheets Data Loaded Successsfully")
             # Pulling ability data
            cursor = conn.execute("SELECT line, ability_id, cost from Datasheets_abilities WHERE datasheet_id=?", (unit_to_load,))
            result = cursor.fetchall()
            for row in result:
                tempItem = {'ability_id': row['ability_id'], 'cost':row['cost']}
                self.ability_list.append(tempItem)
            
            for entry in self.ability_list:
                cursor = conn.execute("SELECT name, description from Abilities WHERE id=?", (entry['ability_id'],))
                result = cursor.fetchone()
                entry['name'] = result['name']
                entry['description'] = stripHTML(result['description'])
           
        
    
    # 'SaveToJSON' Appends the Unit to the end of a JSON file
    # def saveToJSON(self, file_path):

    # 'LoadFromJSON' Appends the Unit to the end of a JSON file
    # def loadFromJSON(self, file_path):
# END of 'Unit' definition

# Testing section
print(DB_PATH)
testUnit = Unit()

testUnit.loadUnitSQLData("000000882")
print("The unit name is " + testUnit.name)
print("The unit role is " + testUnit.role)
print("The unit composition is " + testUnit.composition)
print("The unit transport is " + testUnit.transport)

for entry in testUnit.ability_list:
    print("Ability Name: " + entry['name'])
    print("Ability ID: " + entry['ability_id'])
    print("Ability Cost: " + entry['cost'])
    print("Ability Description: " + entry['description'])