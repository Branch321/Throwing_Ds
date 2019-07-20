# This module will contain a "player" class that will hold all statuses/attributes

import configparser
import datetime

# TODO: Create a class for player status, stats, last roll, session duration, etc....

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

    def __init__(self):
        self.last_roll = {}
        self.benny_counter = 3
        self.traits = {}
        config = configparser.ConfigParser()
        config.read('player.ini')
        for key in config['traits']:
            self.traits[key] = config['traits'][key]
        self.wound_count = int(config['wounds']['wounds'])
        self.fat_count = int(config['fatigue']['fatigue'])
        self.shaken = False
        self.session_duration = datetime.time
        self.incap = False
        self.dead = False
    #def time_to_quit(self):