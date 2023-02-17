import json
# from operator import truediv
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
        # self.crusade_stats = {}

    # load data from a dictionary, which is how units are stored
    # in a JSON file. Dictionaries will ONLY be pulled from said
    # JSON rosters.
    def loadFromDict(self, input_dict):
        self.unit_title = input_dict["unit_title"]
        self.name = input_dict["name"]
        self.faction = input_dict["faction"]
        self.count = input_dict["count"]
        self.power_level = input_dict["power_level"]
        self.leader_name = input_dict["leader_name"]
        self.role = input_dict["role"]
        self.composition = input_dict["composition"]
        self.transport = input_dict["transport"]
        self.chosen_power_text = input_dict["chosen_power_text"]
        self.psychic_text = input_dict["psychic_text"]
        self.model_list = input_dict["model_list"]
        self.wargear_list = input_dict["wargear_list"]
        self.ability_list = input_dict["ability_list"]
        self.chosen_trait_list = input_dict["chosen_trait_list"]
        self.psychic_list = input_dict["psychic_list"]
        self.keywords_list = input_dict["keywords_list"]
        self.crusade_trait_list = input_dict["crusade_trait_list"]
        self.crusade_points = input_dict["crusade_points"]
        self.crusade_xp = input_dict["crusade_xp"]
        self.battle_kills = input_dict["battle_kills"]
        self.total_kills = input_dict["total_kills"]
    # END of 'loadFromDict' method

    # Convert this Unit to a dictionary file, then return the dictionary
    def convertToDict(self):
        output_dict = self.__dict__
        return output_dict

    # Returns boolean value based on whether or not unit has a
    # particular keyword
    def hasKeyword(self, keyword_to_find):
        has_keyword = False
        for entry in self.keywords_list:
            if (entry == keyword_to_find):
                has_keyword = True
        return has_keyword 

    # Adds a wargear item to the Unit's list of wargear.
    # "wargear_to_add" should be a dictionary object
    # def addWargear(self, wargear_to_add):

    # Searches for a wargear with name equal to "wargear_to_remove",
    # then removes it from the list
    # def removeWargear(self, wargear_to_remove)


    #Print unit data to console; only for testing purposes
    def printUnit(self):
        print("The unit name is " + self.name)
        print("The unit role is " + self.role)
        print("The unit composition is " + self.composition)
        
        if self.transport != "":
            print("The unit's transport rule is as follows:" + self.transport)
        else:
            print("This unit is not a transport.")

        for entry in self.ability_list:
            print("Ability Name: " + entry['name'])
            print("Ability ID: " + entry['ability_id'])
            print("Ability Cost: " + entry['cost'])
            print("Ability Description: " + entry['description'])

        for entry in self.keywords_list:
            print(entry + ',')

        for entry in self.model_list:
            print(entry)

        for entry in self.psychic_list:
            print(entry)

        for entry in self.wargear_list:
            print(entry)
    # END of 'printUnit' method

# END of 'Unit' class definition



# Testing section from this point forward; all sections below
# to be cleared upon implementation of integrated testing 