# Throwing_Ds is a dice roller for table top games(mostly Savage Worlds)
# Written in Python 3.6
# External Libraries Needed: Text-to-Speech - pyttsx3 2.71 - https://github.com/nateshmbhat/pyttsx3

import os
import re
import sys
import time

import pyttsx3

import dice
import player


# TODO: Add this to Discord for friends to use
# TODO: Check for luck and great luck edges
# TODO: Add an ascii dice in the far future
# TODO: Need to add a verbosity flag for DEBUG:: messages
# TODO: Add better commenting
# TODO: Need to add a sanitization function to stop program from crashing on bad input
# TODO: Added a text to voice for introduction
# TODO: Added a dice statistics option to print out all the statistics of the current session
# TODO: Create a logger for all dice history


# TODO before release: sanitizer , update player.ini in main menu, output fat/wound, and maybe a logger.
def parse_down(dice_list, all_dice):
    """
    # Purpose: Function that parses user input
    # Pre: dice_list is the user input and all_dice is an object of dice class
    # Post: will modify all_dice.dice_dictionary
    """

    dice_list_split_on_spaces = dice_list.split(' ')
    # parse and form the dictionary to return
    for each_dice in dice_list_split_on_spaces:
        # condition for dice roll
        if 'd' in each_dice:
            split_dice = each_dice.split('d')
            all_dice.dice_dictionary[split_dice[1]] = int(split_dice[0])
        # condition for modifier
        if '-' in each_dice or '+' in each_dice:
            all_dice.dice_dictionary['modifier'] = int(each_dice)


def main_menu():
    """
    # Purpose: Prints out a menu with player status, last roll, and types of commands
    # Pre: None
    # Post: Will print to standard output
    """
    # TODO We need an option to open up your character sheet ("player.ini")
    print("*" * 65)
    print("*" + " " + "Name: " + current_player.name)
    print("*" + " Status - " + "Bennies: " + str(current_player.benny_counter))
    print("*          " + "Wounds: " + str(current_player.wound_count))
    print("*          " + "Fatigue: " + str(current_player.fat_count))
    # FIXME: Need to make the "Last Roll" option look prettier
    print("*" + " Last Roll - " + str(all_dice.last_roll))
    print("*" + " Types of Commands- Roll a dice (Format: 1d10 2d20 -2)")
    print("*" + " " * 20 + "Attribute roll (Format: vigor -2)")
    print("*" + " " * 20 + "Reroll with a benny (Format: benny)")
    print("*" + " " * 20 + "Roll for initiative (Format: init)")
    print("*" + " " * 20 + "Roll for damage (Format: dmg 1d4 -2)")
    print("*" + " " * 20 + "Shaken status (Format: shaken)")
    print("*" + " " * 20 + "Exit this program (Format: exit)")
    print("*" + " " * 20 + "Take a wound (Format: wound)")
    print("*" * 65)


def onWord(name, location, length):
    onWord.index += 1
    print(name, onWord.index)


def intro_banner_voice():
    onWord.index = 0
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')  # getting details of current voice
    engine.setProperty('voice', voices[1].id)  # changing index, changes voices. 1 for female
    rate = engine.getProperty('rate')  # getting details of current speaking rate
    engine.setProperty('rate', 125)  # setting up new voice rate
    engine.connect('started-word', onWord)
    engine.say("Hello, ", "Hello, ")
    onWord.index = 0
    engine.say("I am your Ice Era Assistant.", "I am your Ice Era Assistant.")
    onWord.index = 0
    engine.say("I hope you have fun in tonight's session.", "I hope you have fun in tonight's session.")
    onWord.index = 0
    engine.runAndWait()
    engine.stop()


def intro_banner():
    """
    # Purpose: Welcome banner for startup
    # Pre: None
    # Post: Will print to standard output
    """
    # TODO: Need to multi-thread  the voice to test for the intro_banner function
    # TODO: Add a character selection so you can have multiple
    # TODO: change how this works using callbacks so the prints happen with the voice
    # Below is sample code for text to voice
    # voice_thread = threading.Thread(target=intro_banner_voice)
    # voice_thread.start()
    # intro_banner_voice()
    '''
    time.sleep(.5)
    print("*" * 65)
    print("* ", end='')
    for letter in "Hello,":
        print(letter, end='', flush=True)
        time.sleep(.5)
    print("")
    print("* ", end='')
    time.sleep(2)
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
    '''


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


def sanitize_user_input(command):
    follows_rules = True
    # need to change regular expressions to only allow accepted dice
    dice_regular_expression = re.compile(r"\dd\d")
    modifier_regular_expression = re.compile(r"[+-]\d")
    number_of_modifiers = 0
    possible_options = list(current_player.traits.keys())
    possible_options.extend(
        ["benny", "exit", "wound", "shaken", "init", "dmg", "soak", "heal", "exit", "fatigue", "rest"])
    break_up_command = command.split(' ')
    # FIXME need to check for unique occurence of modifeirs and traits
    for option in break_up_command:
        if option not in possible_options and not dice_regular_expression.match(
                option) and not modifier_regular_expression.match(option):
            follows_rules = False
        if option in possible_options and break_up_command.count(option) > 1:
            follows_rules = False
        if modifier_regular_expression.match(option) and break_up_command.count(option) > 1:
            follows_rules = False
    return follows_rules


# Main Start of Program
if __name__ == '__main__':
    cmd = 'mode 65,40'
    os.system(cmd)
    current_player = player.player()
    all_dice = dice.dice()

    # intro_banner()
    while True:
        main_menu()
        dice_roll = input("* Input: ")
        if not sanitize_user_input(dice_roll):
            print("* Unrecognized Command.")
            print("*" * 65)
        else:
            print("*" * 65)

            # TODO damage for melee weapons includes trait dice
            # For rolling initiative
            # Roll a d20 for init with no modifier and no default d6
            if dice_roll == "init":
                all_dice.pick_your_poison("init", current_player)

            # For rolling traits and any other dice than below
            elif any(elem in dice_roll.split(' ') for elem in current_player.traits.keys()):
                selected_trait = dice_roll.split(' ')[0]
                dice_roll = dice_roll.replace(selected_trait, current_player.traits[selected_trait])
                parse_down(dice_roll, all_dice)
                all_dice.pick_your_poison("traits", current_player)

            # For rolling damage
            elif "dmg" in dice_roll:
                dice_roll = dice_roll.replace("dmg", '')
                parse_down(dice_roll, all_dice)
                all_dice.pick_your_poison("dmg", current_player)

            # For rerolling using bennies
            elif dice_roll == "benny":
                if current_player.benny_counter == 0:
                    print("No more bennies")
                elif all_dice.last_roll_was_crit_fail:
                    print("* You cannot benny if you crit failed last roll.")
                else:
                    current_player.benny_counter -= 1
                    all_dice.pick_your_poison("benny", current_player)

            # For wounds and incapacitation
            # If incapacitated you will stay in loop until you beat a vigor roll of 4
            elif dice_roll == "wound":
                if current_player.wound_count >= 3:
                    current_player.wound_count = 3
                    current_player.incap = True
                while current_player.incap:
                    input("* You are incapacitated. Hit enter to roll a vigor.")
                    dice_roll = current_player.traits['vigor']
                    parse_down(dice_roll, all_dice)
                    all_dice.pick_your_poison("traits", current_player)
                    if all_dice.last_roll_was_crit_fail:
                        death_banner()
                        current_player.dead = True
                    if all_dice.last_actual_roll >= 4:
                        current_player.incap = False
                if current_player.wound_count >= 3:
                    current_player.wound_count = 3
                else:
                    current_player.wound_count += 1

            # For shaken status
            # If shaken you will stay in loop until you beat a spirit roll of 4 or pay a benny
            elif dice_roll == "shaken":
                current_player.shaken = True
                while current_player.shaken:
                    main_menu()
                    user_input = input("* You are shaken. Hit enter to roll a spirit or use a benny:")
                    if user_input == "benny":
                        if current_player.benny_counter == 0:
                            print("* No more bennies")
                        else:
                            current_player.benny_counter -= 1
                            current_player.shaken = False
                            print("* You've used a benny to unshake.")
                    else:
                        dice_roll = current_player.traits['spirit']
                        parse_down(dice_roll, all_dice)
                        all_dice.pick_your_poison("traits", current_player)
                        if all_dice.last_actual_roll >= 4:
                            current_player.shaken = False
                            print("* Your spirit is strong!")
            # For soak rolls
            # Soak rolls will automatically remove wounds
            elif dice_roll == "soak":
                dice_roll = current_player.traits['vigor']
                parse_down(dice_roll, all_dice)
                all_dice.pick_your_poison("soak", current_player)

            # For healing wounds
            elif dice_roll == "heal":
                if current_player.wound_count > 0:
                    current_player.wound_count -= 1
                    print("* " + "One of your wounds has been healed.")
                else:
                    print("* " + "You do not have any wounds to heal.")

            # For fatigue counting
            elif dice_roll == "fatigue":
                if current_player.fat_count == 3:
                    print(current_player.fat_count)
                    current_player.fat_count = 3
                    current_player.incap = True
                    print(current_player.incap)
                else:
                    current_player.fat_count += 1

            # For recovering from fatigue using "rest" command
            elif dice_roll == "rest":
                if current_player.fat_count == 3 and current_player.incap:
                    current_player.fat_count = 0
                    current_player.incap = False
                    print("* " + "You feel rested.")
                else:
                    print("* " + "You aren't quite tired enough to sleep.")

            # To roll death banner
            elif dice_roll == "death":
                death_banner()

            # To exit game
            elif dice_roll == "exit":
                # TODO: Need to write settings and stuff back out to .ini file. prototype function in player class
                print("* " + "You played for ")
                current_player.time_to_quit()
                sys.exit()
            else:
                parse_down(dice_roll, all_dice)
                all_dice.roll_them_bones("custom_roll", current_player)
