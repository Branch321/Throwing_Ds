# Throwing_Ds is a dice roller for table top games(mostly Savage Worlds)
# Written in Python 3.6
# External Libraries Needed: Text-to-Speech - pyttsx3 2.71 - https://github.com/nateshmbhat/pyttsx3

import copy
import random
import sys
import time
import player
# import pyttsx3

'''
# Below is sample code for text to voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
rate = engine.getProperty('rate')   # getting details of current speaking rate
engine.setProperty('rate', 125)     # setting up new voice rate
engine.say("I will speak this text")
engine.runAndWait()
engine.stop()
'''


# TODO: Add this to Discord for friends to use
# TODO: Add an ascii dice in the far future
# TODO: Need to add a verbosity flag for DEBUG:: messages
# TODO: Add better commenting
# TODO: Need to add a sanitization function to stop program from crashing on bad input
# TODO: Need to check for only viable dice (i.e. 1d4,1d6,1d8,1d10,1d20)
# TODO: Added a text to voice for introduction
# TODO: Added a dice statistics option to print out all the statistics of the current session
# TODO: Create a logger for all dice history

def parse_down(dice_list, damage=False):
    """
    # Purpose: Function that parses and sanitizes user input
    # Pre: damage variable determines whether to remove d6 for damage rolls
    # Post: Returns a dictionary of dice options format: {# sided dice: # of rolls,'modifier':0}
    """
    # below takes care of wound and fatigue modifier
    # if current_player.wound_count > 0 or current_player.fat_count > 0:
    #    dice_dictionary = {'modifier': -(current_player.wound_count + current_player.fat_count)}
    dice_dictionary = {'4':0,'6':0, '8':0,'10':0,'12':0,'20':0,'modifier':0}
    dice_list_split_on_spaces = dice_list.split(' ')
    # parse and form the dictionary to return
    for each_dice in dice_list_split_on_spaces:
        # condition for dice roll
        if 'd' in each_dice:
            split_dice = each_dice.split('d')
            dice_dictionary.update({split_dice[1]: split_dice[0]})
        # condition for modifier
        if '-' in each_dice or '+' in each_dice:
            dice_dictionary.update()
            dice_dictionary['modifier'] = str(each_dice)
    print("DEBUG::dice_dictionary at the end of parse_down()::" + str(dice_dictionary))
    return dice_dictionary


def random_dice_generator(dice_dictionary, type_of_roll):
    """
    # Purpose: Randomizes the dice rolls and prints the max of the rolls
    # Pre: must be passed a dictionary with the format {# sided dice: # of rolls,'modifier':0}
    # Post: Prints to stdout
    """

    crit_fail = False
    actual_rolls = []
    modifier = 0

    # Start with modifiers first
    if type_of_roll != "dmg" or type_of_roll != "initiative":
        pass


    # read in the modifier if there is one
    if 'modifier' in dice_dictionary:
        modifier = dice_dictionary['modifier']
    # Copies the roll in case of benny
    current_player.last_roll = copy.deepcopy(dice_dictionary)
    # reads in modifier
    modifier = dice_dictionary['modifier']
    # gets rid of the modifier in dictionary because it is no longer needed
    del dice_dictionary['modifier']
    print("DEBUG::dice_dictionary in random_dice_generator::" + str(dice_dictionary))
    for dice in dice_dictionary.keys():
        for number in range(0, int(dice_dictionary[dice])):
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
        random_quote_index = random.randint(0, len(crit_quote_list))
        print("* " + str(crit_quote_list[random_quote_index]))
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
    return final_roll_with_modifier


def main_menu():
    """
    # Purpose: Prints out a menu with player status, last roll, and types of commands
    # Pre: None
    # Post: Will print to standard output
    """

    print("*" * 65)
    print("*" + " Status - " + "Bennies: " + str(current_player.benny_counter))
    print("*          " + "Wounds: " + str(current_player.wound_count))
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
    print("*" + " " * 20 + "Take a wound (Format: wound)")
    print("*" * 65)


def intro_banner():
    """
    # Purpose: Welcome banner for startup
    # Pre: None
    # Post: Will print to standard output
    """

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


def death_banner():
    """"
    # Purpose: Banner for death
    # Pre: None
    # Post: Will print death banner and exit program
    """

    print("\n" * 40)
    time.sleep(3)
    print("██ ╗  ██ ╗ ██████ ╗  ██ ╗  ██ ╗    ██████ ╗  ██ ╗ ███████ ╗")
    print("╚██ ╗██ ╔╝██ ╔═══██ ╗ ██ ║  ██ ║    ██ ╔═██ ║  ██ ║ ██╔════════╝")
    print(" ╚████ ╔╝ ██ ║   ██ ║ ██ ║  ██ ║    ██ ║ ██ ║  ██ ║ █████ ╗  ")
    print("   ╚██ ╔╝  ██ ║   ██ ║ ██ ║  ██ ║    ██ ║ ██ ║  ██ ║ ██╔═════╝  ")
    print("    ██ ║    ╚█████ ╔╝  █████ ╔╝     █████ ╔╝  ██ ║ ███████ ╗")
    print("    ╚═══╝     ╚════════╝   ╚════════╝      ╚═══════╝   ╚════╝ ╚═══════════╝")
    print("\n" * 10)
    input("Better luck next time. Press enter to exit")
    sys.exit()


# Main Start of Program
current_player = player.player()
# TODO Check for luck and great luck edges
with open("crit_fail_quotes.txt") as file:
    crit_quote_list = file.read().splitlines()
with open("explosion_quotes.txt") as file:
    explosion_quote_list = file.read().splitlines()
# intro_banner()
while True:
    main_menu()
    # TODO: Add skill to options(only have attributes right now)
    dice_roll = input("* Input: ")
    print("*" * 65)
    # Roll a d20 for init with no modifier and no default d6
    if dice_roll == "init":
        print("* Your initiation roll is " + str(random.randint(1, 20)) + '.')
    # This is for shaken status
    elif dice_roll == "shaken":
        current_player.shaken = True
        # If shaken you will stay in loop until you beat a spirit roll of 4 or pay a benny
        while current_player.shaken:
            main_menu()
            user_input = input("* You are shaken. Hit enter to roll a spirit or use a benny:")
            if user_input == "benny":
                if current_player.benny_counter == 0:
                    print("No more bennies")
                else:
                    current_player.benny_counter -= 1
                    current_player.shaken = False
                    print("You've used a benny to unshake.")
            else:
                dice_roll = current_player.traits['spirit']
                dice_options = parse_down(dice_roll)
                spirit_check_value = random_dice_generator(dice_options)
                if spirit_check_value >= 4:
                    current_player.shaken = False
    # Rerolls the last current_player.last_roll
    elif dice_roll == "benny":
        # FIXME Not supposed to be able to use benny on crit fails
        if current_player.benny_counter == 0:
            print("No more bennies")
        else:
            current_player.benny_counter -= 1
            random_dice_generator(current_player.last_roll)
    # Rolls a damage roll with modifier, does not roll a default 1d6
    elif "dmg" in dice_roll:
        del dice_roll[0]
        dice_options = parse_down(dice_roll, True)
        random_dice_generator(dice_options)
    # Rolls an attribute roll with modifier based on the traits dictionary
    elif dice_roll in current_player.traits.keys():
        # FIXME Fix dice roll for damage using trait dice
        dice_roll = current_player.traits[dice_roll]
        dice_options = parse_down(dice_roll)
        random_dice_generator(dice_options)
    # Exit condition
    elif dice_roll == "exit":
        # TODO: Need to write settings and stuff back out to .ini file
        print("* You played for ")
        sys.exit()
    # wound modifier
    elif dice_roll == "wound":
        # FIXME Incapacitation only triggers once before not triggering
        if current_player.wound_count >= 3:
            current_player.incap = True
            current_player.wound_count = 3
        # If incapacitated you will stay in loop until you beat a vigor roll of 4
        while current_player.incap:
            main_menu()
            input("* You are incapacitated. Hit enter to roll a vigor")
            dice_roll = current_player.traits['vigor']
            dice_options = parse_down(dice_roll)
            vigor_check_value = random_dice_generator(dice_options)
            if vigor_check_value == 1:
                death_banner()
                current_player.dead = True
            if vigor_check_value >= 4:
                current_player.incap = False
        else:
            current_player.wound_count += 1
            # If incapacitated crit fail will cause death
            # If incapacitated success on vigor will stablize player
    # fatigue modifier
    elif dice_roll == "fatigue":
        current_player.fat_count += 1
    # all other custom dice rolls
    elif dice_roll == "death":
        death_banner()
    # Quick command for death banner

    else:
        dice_options = parse_down(dice_roll)
        random_dice_generator(dice_options)
