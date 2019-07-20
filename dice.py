#class to hold all the dice configuration
import random
import copy


class dice:
    """
    # Purpose:
    # Variables:
    """
    def __init__(self):
        self.dice_dictionary = {'4': 0,'6': 0, '8': 0,'10': 0,'12': 0,'20': 0,'modifier':0}
        self.last_roll = {}
        self.number_of_explosions = 0
        self.last_roll_was_crit_fail = False
        with open("crit_fail_quotes.txt") as file:
            self.crit_quote_list = file.read().splitlines()
        with open("explosion_quotes.txt") as file:
            self.explosion_quote_list = file.read().splitlines()

    def roll_them_bones(self, type_of_roll, current_player=None):
        #FIXME: fix the documentation
        """
        # Purpose: Randomizes the dice rolls and prints the max of the rolls
        # Pre: type_of_roll is a 'iniative','benny', or 'damage'
        #      current_layer is needed for the wound and fatigue modifiers
        #      you need to set the dice object's dice_dictionary before calling this function
        # Post: Prints to stdout and resets the dice object's dice_dictionary
        #       sets last_roll, number_of_explosions, and last_roll_was_crit_fail
        """

        # FIXME Enable using benny to reroll initiative
        if type_of_roll=='initiative':
            print("Your initiative is " + str(random.randint(1,20)) + ".")
        else:
            crit_fail = False
            actual_rolls = []

            if not type_of_roll =='benny':
                # modifier for wounds and fatigue are applied
                if current_player.wound_count > 0 or current_player.fat_count > 0:
                    self.dice_dictionary['modifier'] += -(current_player.wound_count + current_player.fat_count)
                # adds a wild 1d6 if it is not a damage roll
                if type_of_roll != "damage":
                    self.dice_dictionary['6'] += 1
                # copy the current dice configuration into last_roll in case of benny next turn
                self.last_roll = copy.deepcopy(self.dice_dictionary)
            # if the type_of_roll is a benny then copy the last_roll back into dice_dictionary and roll with previous
            # configuration
            else:
                self.dice_dictionary = copy.deepcopy(self.last_roll)
            # Set and delete modifier from dice_dictionary
            modifier = self.dice_dictionary['modifier']
            del self.dice_dictionary['modifier']
            print("DEBUG::modifier:: " + str(modifier))
            print("DEBUG::dice_dictionary in random_dice_generator::" + str(self.dice_dictionary))
            for dice in self.dice_dictionary.keys():
                for number in range(0, int(self.dice_dictionary[dice])):
                    current_roll = random.randint(1, int(dice))
                    while current_roll == int(dice):
                        self.number_of_explosions += 1
                        print("DEBUG::current_roll::" + str(current_roll))
                        # FIXME: It needs to count the explosions and output the final value
                        print("There has been an explosion!")
                        current_roll += random.randint(1, int(dice))
                    actual_rolls.append(current_roll)
                    print("DEBUG::number_of_explosions" + str(self.number_of_explosions))
            print("DEBUG::actual_roll " + str(actual_rolls))
            final_roll = max(actual_rolls)
            # below deals with crit fail roll
            # FIXME: if you have multiple dice rolls, if over half crit fail then the entire roll is crit fail
            if final_roll == 1:
                # testing the for loop below
                random_quote_index = random.randint(0, len(self.crit_quote_list)-1)
                print("* " + str(self.crit_quote_list[random_quote_index]))
                crit_fail = True
                final_roll_with_modifier = final_roll
            else:
                final_roll_with_modifier = final_roll + int(modifier)
            # if the dice is below 1 set to 1
            if final_roll_with_modifier < 0:
                final_roll_with_modifier = 0
            # FIXME: there may still be instances where you need to print out the dice roll with the modifier
            if not crit_fail:
                print("* " + "Dice Roll is " + str(final_roll_with_modifier) + ".")
            self.last_roll_was_crit_fail = crit_fail
            self.reset_roll()

    def reset_roll(self):
        """
        # Purpose:
        # Pre:
        # Post:
        """
        # FIXME: fix all the documentation
        self.dice_dictionary = {'4': 0,'6': 0, '8': 0,'10': 0,'12': 0,'20': 0,'modifier':0}
        self.explosions = 0
