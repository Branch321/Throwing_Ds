# This module will contain a "player" class that will hold all statuses/attributes

import configparser
import datetime

class player:
    """
    # Purpose: This class will hold all the player stats and statuses
    # Variables: last_roll - holds the player's last roll
    #            benny_counter - # of bennies player has
    #            traits - holds attributes and skills
    #            wound_count - # of wounds the player has
    #            fat_count - # of fatigue the player has
    #            shaken - boolean determines if player is shaken or not
    #            session_duration - holds the time the player started the ice era assistant
    #            incap - boolean determines if player is incapacitated
    """

    def __init__(self,name_of_character):
        #self.last_roll = {}
        self.benny_counter = 3
        self.traits = {}
        self.weapons_dictionary = {}
        self.config = configparser.ConfigParser()
        self.config.read('characters/' + name_of_character+'.ini')
        self.name_of_character = name_of_character
        for key in self.config['traits']:
            self.traits[key] = self.config['traits'][key]
        self.wound_count = int(self.config['wounds']['wounds'])
        self.fat_count = int(self.config['fatigue']['fatigue'])
        self.shaken = False
        self.session_duration = datetime.time
        self.incap = False
        self.name = self.config['name']['name']
        for weapon in self.config['weapons']:
            self.weapons_dictionary[weapon] = self.config['weapons'][weapon]
    #we will use this function for exiting the program and writing all variables back out to player.ini
    def time_to_quit(self):
        """
        # Purpose:
        # Pre:
        # Post:
        """
        self.config.set("wounds","wounds", str(self.wound_count))
        self.config.set("fatigue","fatigue",str(self.fat_count))
        #with open("player.ini",'w') as file:
        #    self.config.write(file)
