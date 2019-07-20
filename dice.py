#class to hold all the dice
import random
import copy

class dice:
    def __init__(self):
        self.dice_dictionary = {'4': 0,'6': 0, '8': 0,'10': 0,'12': 0,'20': 0,'modifier':0}
        self.last_roll = {}
        self.number_of_explosions = 0
        with open("crit_fail_quotes.txt") as file:
            self.crit_quote_list = file.read().splitlines()
        with open("explosion_quotes.txt") as file:
            self.explosion_quote_list = file.read().splitlines()

    def roll_them_bones(self, type_of_roll, current_player=None):
        #FIXME: fix the documentation
        """
        # Purpose: Randomizes the dice rolls and prints the max of the rolls
        # Pre: must be passed a dictionary with the format {# sided dice: # of rolls,'modifier':0}
        # Post: Prints to stdout
        """

        if type_of_roll=='initiative':
            print("Your initiative is " + str(random.randint(1,20)) + ".")
        else:
            print("DEBUG::State of dice class::" + str(self.dice_dictionary))
            crit_fail = False
            actual_rolls = []
            # modify the modifier
            if current_player.wound_count > 0 or current_player.fat_count > 0:
                self.dice_dictionary['modifier'] += -(current_player.wound_count + current_player.fat_count)
            #copying roll into last roll for bennies
            self.last_roll = copy.deepcopy(self.dice_dictionary)
            # deleting uneeded modifiers
            modifier = self.dice_dictionary['modifier']
            del self.dice_dictionary['modifier']
            # done modifying the modifier
            print("DEBUG::modifier:: " + str(modifier))
            # add default d6 when not a damage or initiative roll
            if type_of_roll != "damage":
                self.dice_dictionary['6'] += 1
            # below takes care of wound and fatigue modifier
            print("DEBUG::dice_dictionary in random_dice_generator::" + str(self.dice_dictionary))
            # TODO: need to add to self.last_roll()
            for dice in self.dice_dictionary.keys():
                for number in range(0, int(self.dice_dictionary[dice])):
                    current_roll = random.randint(1, int(dice))
                    while current_roll == int(dice):
                        # FIXME: It needs to count the explosions and output the final value
                        print("There has been an explosion!")
                        current_roll = current_roll + random.randint(1, int(dice))
                    actual_rolls.append(current_roll)
            print("DEBUG::actual_roll " + str(actual_rolls))
            final_roll = max(actual_rolls)
            # below deals with crit fail roll
            # FIXME: if you have multiple dice rolls, if over half crit fail then the entire roll is crit fail
            if final_roll == 1:
                random_quote_index = random.randint(0, len(self.crit_quote_list))
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
            self.reset_roll()
            return final_roll_with_modifier

    def reset_roll(self):
        # FIXME: fix all the documentation
        self.dice_dictionary = {'4': 0,'6': 0, '8': 0,'10': 0,'12': 0,'20': 0,'modifier':0}
        self.explosions = 0
