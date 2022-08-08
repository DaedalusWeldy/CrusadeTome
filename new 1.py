import json
import sqlite3

# ************
# DEFINITIONS
# ************

# global variable to declare the file path of DB 
DB_PATH = "WahapediaSQL.db"

class Unit:
    def __init__(self):
        self.unit_name = "New Unit"
        self.unit_faction = "None"
        self.unit_count = 0
        self.unit_leader_name = "Unit Leader"
        self.unit_role = "None"
        self.unit_composition = "None"
        self.unit_transport = "Not a transport"
        self.unit_priest_text = "Not a priest"
        self.unit_psychic_text = "Not a psychic"
        # unitStats follows the same sequence that 
        # official Warhammer 40k datasheets use
        self.unit_stats = {"move":0,"weapon_skill":0,
                          "ballistic_skill":0,"strength":0,
                          "toughness":0,"wounds":0, "attacks":0,
                          "leadership":0,"save":0}
        self.leader_stats = {"move":0,"weapon_skill":0,
                          "ballistic_skill":0,"strength":0,
                          "toughness":0,"wounds":0,"attacks":0,
                          "leadership":0,"save":0}
        self.unit_weapon_list = []
        self.unit_ability_list = []
        self.unit_priest_list = []
        self.unit_psychic_list = []
        self.unit_crusade_trait_list = []
        self.unit_crusade_xp = []
        self.unit_battle_kills = {"ranged":0, "melee":0, "psychic":0}
        self.unit_total_kills = {"ranged":0, "melee":0, "psychic":0}

    # 'LoadUnitData' loads data for the chosen unit from WahapediaSQL.db
    # unit_to_load should be the string of the datasheet ID
    def loadUnitSQLData(self, unit_to_load):
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT name, role, unit_composition, transport, priest, psyker, faction_id FROM Datasheets WHERE id=?", (unit_to_load))
            result = cursor.fetchone()
            self.unit_name = result['name']
            self.unit_role = result['role']
            self.unit_composition = result['unit_composition']
        
    
    # 'SaveToJSON' Appends the Unit to the end of a JSON file
    # def saveToJSON(self, file_path):

    # 'LoadFromJSON' Appends the Unit to the end of a JSON file
    # def loadFromJSON(self, file_path):