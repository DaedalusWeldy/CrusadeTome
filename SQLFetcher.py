# SQLFetcher class
# To act as a go-between for any function that needs to access
# the SQLite database.

from Unit import Unit
import os
import re
import sqlite3

class SQLFetcher:
    def __init__(self):
        # global variable to declare the file path of DB
        # copied from https://help.pythonanywhere.com/pages/NoSuchFileOrDirectory/
        self.THIS_FOLDER = os.path.dirname(__file__)
        self.DB_PATH = os.path.join(self.THIS_FOLDER, r"WahapediaSQL.db")

        self.conn = sqlite3.connect(self.DB_PATH)
        self.conn.row_factory = sqlite3.Row

        self.unit_to_output = Unit()

    # Strips extra HTML formatting from input_string, returns
    # clean string of text
    def stripHTML(self, input_string):
        return re.sub("<[^>]+>", '', input_string)

    # Method used to clear all data from the current Unit object, start over
    def clearCurrentUnit(self):
        self.unit_to_output = Unit()

    # Obtains basic clerical data on the unit like it's name, unit size, psyker 
    # capabilites, etc.
    def fetchUnitProfile(self, unit_id_to_load):
        # Pulling raw info from Datasheets
        # Apologies, SQL string will not split neatly onto multiple lines
        cursor = self.conn.execute("SELECT name, role, unit_composition, transport, priest, psyker, faction_id from Datasheets WHERE id=?", (unit_id_to_load,))
        result = cursor.fetchone()
        # save information from SQL call into the unit_to_output
        self.unit_to_output.name = result["name"]
        self.unit_to_output.role = result["role"]
        self.unit_to_output.composition = self.stripHTML(result["unit_composition"])
        if result["transport"] != "":
            self.unit_to_output.transport = self.stripHTML(result["transport"])
        if result["priest"] != "":
            self.unit_to_output.chosen_power_text = self.stripHTML(result['priest'])
        if result["psyker"] != "":
            self.unit_to_output.psychic_text = result["psyker"]
        self.unit_to_output.faction = result["faction_id"]
    
    # Fetches all of the ability names (and associated text) of the selected unit
    def fetchUnitAbilities(self, unit_id_to_load):
        # Pulling raw info from Datasheets
        # Pulling ability pointer data
        cursor = self.conn.execute("SELECT line, ability_id, cost from Datasheets_abilities WHERE datasheet_id=?", (unit_id_to_load,))
        result = cursor.fetchall()
        for row in result:
            tempItem = {"ability_id": row["ability_id"], "cost":row["cost"]}
            self.unit_to_output.ability_list.append(tempItem)
        # Using pointer data from previous step, pull actual text of abilities 
        for entry in self.unit_to_output.ability_list:
            cursor = self.conn.execute("SELECT name, description from Abilities WHERE id=?", (entry["ability_id"],))
            result = cursor.fetchone()
            entry["name"] = result["name"]
            entry["description"] = self.stripHTML(result["description"])

    def fetchUnitKeywords(self, unit_id_to_load):
        # Pulling in unit's associated keywords
        cursor = self.conn.execute("SELECT keyword, model from Datasheets_keywords WHERE datasheet_id=?", (unit_id_to_load,))
        result = cursor.fetchall()
        for row in result:
            if row["model"] != "":
                self.unit_to_output.keywords_list.append('' + row["keyword"] + '(' + row["model"] + ')')
            else:
                self.unit_to_output.keywords_list.append(row["keyword"])

    def fetchUnitStats(self, unit_id_to_load):
        cursor = self.conn.execute("SELECT name, M, WS, BS, S, T, W, A, Ld, Sv, Cost, cost_description," +
            "models_per_unit from Datasheets_models WHERE datasheet_id=?", (unit_id_to_load,))
        result = cursor.fetchall()
        for row in result:
            model_input = {"model_name": row["name"],
                "model_M": row["M"], "model_WS": row["WS"],
                "model_BS": row["BS"], "model_S": row["S"],
                "model_T": row["T"], "model_W": row["W"],
                "model_A": row["A"], "model_Ld": row["Ld"],
                "model_Sv": row["Sv"], "model_count": 0}
            self.unit_to_output.model_list.append(model_input)

    def fetchUnitWargear(self, unit_id_to_load):
        temp_wargear_list = []
        cursor = self.conn.execute("SELECT wargear_id, cost from Datasheets_wargear WHERE datasheet_id=?", (unit_id_to_load,))
        result =cursor.fetchall()
        for row in result:
            wargear_input = {"wargear_id": row["wargear_id"],
                                "wargear_cost": row["cost"]}
            self.unit_to_output.wargear_list.append(wargear_input)
        # Pulling data for each wargear piece
        for entry in self.unit_to_output.wargear_list:
            temp_wargear = entry
            cursor = self.conn.execute("SELECT name, type, description from Wargear WHERE id=?", (entry["wargear_id"],))
            cursor2 = self.conn.execute("SELECT name, range, type, S, AP, D, abilities from Wargear_list WHERE wargear_id=?", (entry["wargear_id"],))
            result = cursor.fetchone()
            result2 = cursor2.fetchall()
            temp_wargear["wargear_name"] = result["name"]
            temp_wargear["wargear_type"] = result["type"]
            temp_wargear["wargear_description"] = result["description"]
            # If result2 is only one entry, add descriptions to existing list item
            # Otherwise, add sub-gear below it on the list for each profile
            if len(result2) == 1:
                temp_wargear["wargear_range"] = result2[0]["range"]
                temp_wargear["wargear_type"] = result2[0]["type"]
                temp_wargear["wargear_s"] = result2[0]["S"]
                temp_wargear["wargear_ap"] = result2[0]["AP"]
                temp_wargear["wargear_d"] = result2[0]["D"]
                temp_wargear["wargear_abilities"] = self.stripHTML(result2[0]["abilities"])
                temp_wargear["is_active"] = False
                temp_wargear_list.append(temp_wargear)
            elif len(result2) > 1:
                temp_wargear_list.append(temp_wargear)
                for sub_entry in result2:
                    shot_type = {"wargear_name":sub_entry["name"], "wargear_type":sub_entry["type"],
                                "wargear_s":sub_entry["S"], "wargear_ap":sub_entry["AP"],
                                "wargear_d":sub_entry["d"], "wargear_abilities":self.stripHTML(sub_entry["abilities"]),
                                "is_active": False}
                    temp_wargear_list.append(shot_type)
            else:
                print("ERROR: Incorrect wargear generation!")
        # Apply the new, complete list of wargear, overwriting the current one
        self.unit_to_output.wargear_list = temp_wargear_list

    def fetchUnitPsykerData(self, unit_id_to_load):
        if self.unit_to_output.psychic_text != "No psychic powers":
            cursor = self.conn.execute("SELECT roll, name, type, description from PsychicPowers WHERE faction_id=?", (self.unit_to_output.faction,))
            result =cursor.fetchall()
            for row in result:
                psychic_power = {"power_name": row["name"], "power_roll": row["roll"],
                                "power_type":row["type"], "power_description": self.stripHTML(row["description"]),
                                "is_active": False}
                self.unit_to_output.psychic_list.append(psychic_power)

    # Run the various queries, and return a completed Unit object
    # "unit_id" must be one of the two-or-three-letter combinations
    # used by the SQL data from Wahapedia 
    def fetchAllUnitData(self, unit_id):
        self.clearCurrentUnit()
        self.fetchUnitProfile(unit_id)
        self.fetchUnitAbilities(unit_id)
        self.fetchUnitKeywords(unit_id)
        self.fetchUnitStats(unit_id)
        self.fetchUnitWargear(unit_id)
        self.fetchUnitPsykerData(unit_id)
        return self.unit_to_output

    # fetch a list of all of the factions in the game, as well as their
    # two-or-three-letter faction ID
    def fetchFactionList(self):
        faction_list = []
        
        # TEST
        # Coconut.jpg: without a fake entry on the first entry of the faction list,
        # the first faction listed does not work.
        # faction_list.append({"id":"TST", "name":"Enter a faction..."})
        
        cursor = self.conn.execute("SELECT id, name from Factions", ())
        result = cursor.fetchall()
        for entry in result:
            faction_list.append(entry)
        return faction_list


    # Returns a list of Unit objects, containing all Units that belong
    # to the chosen faction
    def fetchUnitList(self, faction):
        list_of_id_nums = []
        list_of_units = []

        # Compile a list of all ID numbers belonging to the faction specified
        cursor = self.conn.execute("SELECT id from Datasheets WHERE faction_id=?", (faction,))
        result = cursor.fetchall()
        for entry in result:
            list_of_id_nums.append(str(entry["id"]))

        for entry in list_of_id_nums:
            list_of_units.append(self.fetchAllUnitData(entry))
        
        return list_of_units


# Testing section: will be deleted once testing is completed
# test_fetcher = SQLFetcher()
# unit_test = test_fetcher.fetchAllUnitData("000000882")
# unit_test.printUnit()