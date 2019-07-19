#This module will contain a "player" class that will hold all statuses/attributes

import configparser

class player:
    """
    # Purpose:
    # Variables: last_roll - holds the player's last roll
    #            benny_counter - # of bennies player has
    #            traits - holds attributes and skills
    #            wound_count - # of wounds the player has
    """

    def __init__(self):
        self.last_roll = {}
        self.benny_counter = 3
        self.traits = {}
        config = configparser.ConfigParser()
        config.read('player.ini')
        for key in config['traits']:
            self.traits[key] = config['traits'][key]
        self.wound_count = config['wounds']['wounds']
