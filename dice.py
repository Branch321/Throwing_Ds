# class to hold all the dice configuration
import copy
import random


class dice:
    """
    # Purpose:
    # Variables:
    """

    def __init__(self):
        self.dice_dictionary = {'4': 0, '6': 0, '8': 0, '10': 0, '12': 0, '20': 0, 'modifier': 0}
        self.last_roll = {}
        self.number_of_explosions = 0
        self.last_roll_was_crit_fail = False
        self.last_actual_roll = 0
        with open("crit_fail_quotes.txt") as file:
            self.crit_quote_list = file.read().splitlines()
        with open("explosion_quotes.txt") as file:
            self.explosion_quote_list = file.read().splitlines()

    def roll_them_bones(self, type_of_roll, allow_explosions=True):
        # FIXME: fix the documentation
        """
        # Purpose: Randomizes the dice rolls and prints the max of the rolls
        # Pre: type_of_roll is a 'iniative','benny', or 'damage'
        #      current_layer is needed for the wound and fatigue modifiers
        #      you need to set the dice object's dice_dictionary before calling this function
        # Post: Prints to stdout and resets the dice object's dice_dictionary
        #       sets last_roll, number_of_explosions, and last_roll_was_crit_fail
        """

        crit_fail = False
        actual_rolls = []

        self.last_roll = copy.deepcopy(self.dice_dictionary)
        # if the type_of_roll is a benny then copy the last_roll back into dice_dictionary and roll with previous
        # configuration
        # Set and delete modifier from dice_dictionary
        modifier = self.dice_dictionary['modifier']
        del self.dice_dictionary['modifier']
        for dice in self.dice_dictionary.keys():
            for number in range(0, int(self.dice_dictionary[dice])):
                current_roll = random.randint(1, int(dice))
                if allow_explosions:
                    while current_roll == int(dice):
                        self.number_of_explosions += 1
                        current_roll = random.randint(1, int(dice))
                actual_rolls.append(current_roll + self.number_of_explosions * int(dice))
                if self.number_of_explosions >= 1:
                    print("* " + "There were " + str(
                        self.number_of_explosions) + " explosions " + "on the " + dice + " die" if
                          self.number_of_explosions > 1  else "* " + "There was " + str(self.number_of_explosions) + " explosion " + "on the " + dice + " die")
                self.number_of_explosions = 0
        print("* " + "Your rolls before modifiers were: " + str(actual_rolls)[1:-1])
        print("* " + "The modifiers used were: " + str(modifier))
        final_roll = max(actual_rolls)
        # below deals with crit fail roll
        # FIXME: if you have multiple dice rolls, if over half crit fail then the entire roll is crit fail
        if final_roll == 1:
            # testing the for loop below
            random_quote_index = random.randint(0, len(self.crit_quote_list) - 1)
            print("* " + str(self.crit_quote_list[random_quote_index]))
            crit_fail = True
            final_roll_with_modifier = final_roll
        else:
            final_roll_with_modifier = final_roll + int(modifier)
        # if the dice is below 1 set to 1
        if final_roll_with_modifier < 0:
            final_roll_with_modifier = 0
        if not crit_fail:
            print("* " + "Dice Roll is " + str(final_roll_with_modifier) + ".")
        self.last_roll_was_crit_fail = crit_fail
        self.reset_roll()
        self.last_actual_roll = final_roll_with_modifier

    def pick_your_poison(self, type_of_roll, current_player):
        """
        # Purpose:
        # Pre:
        # Post:
        """

        # this is the function that will choose type of rolls and apply modifiers then roll_them_bones will do actual rolling
        if type_of_roll == "init":
            self.dice_dictionary["20"] = 1
            self.roll_them_bones("init", False)
            # Initiative: does not explode - does not use wild die - not modified by wounds and fatigue - not modified by custom modifiers - roll 1d20
        elif type_of_roll == "benny":
            self.dice_dictionary = copy.deepcopy(self.last_roll)
            self.roll_them_bones("benny")
        elif type_of_roll == "dmg":
            self.roll_them_bones("dmg")
            # Damage: does explode - does not use wild die - not modified by wounds and fatigue - modified by custom modifiers
        elif type_of_roll == "traits":
            self.dice_dictionary["6"] += 1
            if current_player.wound_count > 0 or current_player.fat_count > 0:
                self.dice_dictionary["modifier"] += -(current_player.wound_count + current_player.fat_count)
            self.roll_them_bones("traits")
            # Trait: does explode - uses a wild die - modified by wounds and fatigue - modified by custom modifiers
        elif type_of_roll == "soak":
            if current_player.wound_count > 0 and current_player.benny_counter >= 0:
                self.dice_dictionary["6"] += 1
                self.dice_dictionary["modifier"] += -(current_player.wound_count + current_player.fat_count)
                current_player.benny_counter -= 1
                self.roll_them_bones("soak")
                if self.last_actual_roll % 4 == 0:
                    soak_roll = self.last_actual_roll / 4
                    current_player.wound_count -= soak_roll
                    print("That didn't hurt so bad.")
            else:
                print("You don't have any bennies left")
            # Soak and Heals - uses wild die - modified by wounds and fatigue - modified by custom modifiers
        else:
            self.roll_them_bones("custom")
            # Custom: does explode - does not use wild die - not modified by wounds and fatigue - modified by custom modifiers

    def reset_roll(self):
        # FIXME: fix all the documentation
        """
        # Purpose:
        # Pre:
        # Post:
        """
        self.dice_dictionary = {'4': 0, '6': 0, '8': 0, '10': 0, '12': 0, '20': 0, 'modifier': 0}
        self.explosions = 0
