# Throwing_Ds is a dice roller for table top games(mostly Savage Worlds)
# Written in Python 3.6
import configparser
import copy
import random
import time
import player

# TODO: Add this to Discord for friends to use
# TODO: Add an ascii dice in the far future
# TODO: Need to add a verbosity flag for DEBUG:: messages
# TODO: Add better commenting
# TODO: MOST-IMPORTANT: Add a state for wounds, shaken/unshaken
# TODO: Need to add a sanitization function to stop program from crashing on bad input
# TODO: Need to check for only viable dice (i.e. 1d4,1d6,1d8,1d10,1d20)
# TODO: Added a text to voice for introduction
# TODO: Add fatigue to play status

# Purpose: Function that parses and sanitizes user input
# Pre: damage variable determines whether to remove d6 for damage rolls
# Post: Returns a dictionary of dice options format: {# sided dice: # of rolls,'modifier':0}
def parse_down(dice_list, damage=False):
    if current_player.wound_count > 0 or current_player.fat_count > 0:
        dice_dictionary = {'modifier': -(current_player.wound_count + current_player.fat_count)}
    else:
        dice_dictionary = {'modifier': 0}
    # initialize dice_dictionary with 1d6 always because Savage Worlds specific dice roller
    if not damage:
        dice_dictionary['6'] = '1'
    # parse and form the dictionary to return
    for each_dice in dice_list:
        # condition for dice roll
        if 'd' in each_dice:
            split_dice = each_dice.split('d')
            dice_dictionary.update({split_dice[1]: split_dice[0]})
        # condition for modifier
        if '-' in each_dice or '+' in each_dice:
            dice_dictionary['modifier'] += int(each_dice)
            # dice_dictionary.update({'modifier': each_dice})
    return dice_dictionary


# Purpose: Randomizes the dice rolls and prints the max of the rolls
# Pre: must be passed a dictionary with the format {# sided dice: # of rolls,'modifier':0}
# Post: Prints to stdout
def random_dice_generator(dice_dictionary):
    # Stores all rolls
    actual_rolls = []
    current_player.last_roll = copy.deepcopy(dice_dictionary)
    # reads in modifier
    modifier = dice_dictionary['modifier']
    # gets rid of the modifier in dictionary because it is no longer needed
    del dice_dictionary['modifier']
    for dice in dice_dictionary.keys():
        for number in range(0, int(dice_dictionary[dice][0])):
            current_roll = random.randint(1, int(dice))
            while current_roll == int(dice):
                # FIXME: It needs to count the explosions and output the final value
                print("There has been an explosion!")
                current_roll = current_roll + random.randint(1, int(dice))
            actual_rolls.append(current_roll)
    final_roll = max(actual_rolls)
    # below deals with crit fail roll
    # FIXME: if crit roll you do not need to output a 1
    if final_roll == 1:
        random_quote_index = random.randint(0, len(crit_quote_list))
        print("* " + str(crit_quote_list[random_quote_index]))
    # apply modifier
    final_roll_with_modifier = final_roll + int(modifier)
    # if the dice is below 1 set to 1
    if final_roll_with_modifier < 1:
        final_roll_with_modifier = 1
    print("* " + "Dice Roll is " + str(final_roll_with_modifier) + ".")
    return final_roll_with_modifier


# Purpose: Prints out a menu with player status, last roll, and types of commands
# Pre: None
# Post: Will print to standard output
def main_menu():
    print("*" * 65)
    print("*" + " Status - " + "Bennies: " + str(current_player.benny_counter))
    print("*           " + "Wounds: " + str(current_player.wound_count))
    print("*          " + "Fatigue: " + str(current_player.fat_count))
    # FIXME: Need to make the "Last Roll" option look prettier
    print("*" + " Last Roll - " + str(current_player.last_roll))
    print("*" + " Types of Commands- Roll a dice (Format: 1d10 2d20 -2)")
    print("*" + " " * 20 + "Attribute roll (Format: vigor -2)")
    print("*" + " " * 20 + "Reroll with a benny (Format: benny)")
    print("*" + " " * 20 + "Roll for initiative (Format: init)")
    print("*" + " " * 20 + "Roll for damage (Format: dmg 1d4 -2)")
    print("*" + " " * 20 + "Shaken status (Format: shaken)")
    print("*" + " " * 20 + "Exit this program (Format: exit)")
    print("*" * 65)


# Purpose: Welcome banner for startup
# Pre: None
# Post: Will print to standard output
def intro_banner():
    print("*" * 65)
    print("* ", end='')
    for letter in "Hello,":
        print(letter, end='', flush=True)
        time.sleep(.3)
    print("")
    print("* ", end='')
    time.sleep(1)
    for letter in "I am your Ice Era Assistant.":
        print(letter, end='', flush=True)
        time.sleep(.1)
    print("")
    print("* ", end='')
    for letter in "I hope you have fun in tonight's session.":
        print(letter, end='', flush=True)
        time.sleep(.1)
    print("")
    print("* ", end='')
    print("Loading", end='')
    time.sleep(1)
    for letter in "....":
        print(letter, end='', flush=True)
        time.sleep(1)
    print("")
    time.sleep(1)


# Main Start of Program
current_player = player.player()
# TODO Check for luck and great luck edges
config = configparser.ConfigParser()
config.read('player.ini')
with open("crit_fail_quotes.txt") as file:
    crit_quote_list = file.read().splitlines()
with open("explosion_quotes.txt") as file:
    explosion_quote_list = file.read().splitlines()
#intro_banner()
while True:
    main_menu()
    # TODO: Add skill to options(only have attributes right now)
    dice_roll = input("* Input: ")
    print("*" * 65)
    # Roll a d20 for init with no modifier
    if dice_roll == "init":
        # FIXME: You can spend a benny to reroll init, need to set the default d6 to false
        print("* Your initiation roll is " + str(random.randint(1, 20)) + '.')
    # If shaken you will stay in loop until you beat a spirit roll of 4
    elif dice_roll == "shaken":
        # TODO: if player spends a benny you can immediately become unshaken
        shaken = True
        while shaken:
            input("* You are shaken. Hit enter to roll a spirit.")
            dice_roll = current_player.traits['spirit']
            dice_roll = dice_roll.split(' ')
            dice_options = parse_down(dice_roll)
            spirit_check_value = random_dice_generator(dice_options)
            if spirit_check_value>=4:
                shaken = False
    # Rolls a damage roll with modifier, does not roll a default 1d6
    elif dice_roll == "benny":
        if current_player.benny_counter == 0:
            print("No more bennies")
        else:
            current_player.benny_counter -= 1
            random_dice_generator(current_player.last_roll)
    elif "dmg" in dice_roll:
        dice_roll = dice_roll.split(' ')
        del dice_roll[0]
        dice_options = parse_down(dice_roll, True)
        random_dice_generator(dice_options)
    # Rolls an attribute roll with modifier based on the options dictionary
    elif dice_roll in current_player.traits.keys():
        dice_roll = current_player.traits[dice_roll]
        dice_roll = dice_roll.split(' ')
        dice_options = parse_down(dice_roll)
        random_dice_generator(dice_options)
    # Exit condition
    elif dice_roll == "exit":
        # TODO: Need to write settings and stuff back out to .ini file
        exit()
    # All standard dice rolls
    elif dice_roll == "wound":
        current_player.wound_count+=1
        # Wound modifier
    elif dice_roll == "fatigue":
        current_player.fat_count+=1
        # Fatigue modifier
    else:
        dice_roll = dice_roll.split(' ')
        dice_options = parse_down(dice_roll)
        random_dice_generator(dice_options)
