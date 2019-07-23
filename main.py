# Throwing_Ds is a dice roller for table top games(mostly Savage Worlds)
# Written in Python 3.6
# External Libraries Needed: Text-to-Speech - pyttsx3 2.71 - https://github.com/nateshmbhat/pyttsx3

import os
import re
import sys
import threading
import time
from ftplib import FTP

import pyttsx3

import dice
import player


# TODO: Add this to Discord for friends to use
# TODO: Check for luck and great luck edges
# TODO: Add an ascii dice in the far future
# TODO: Need to add a verbosity flag for DEBUG:: messages
# TODO: Add better commenting
# TODO: Added a dice statistics option to print out all the statistics of the current session
# TODO: Create a logger for all dice history
# FIXME: need to do a dice_roll.split() in the main program because it is the first thing we call in parse_down() and sanitize_user_input()
# TODO: add a full option list in main function for user_input
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
    print("*" + " Types of Commands - Roll a dice (Format: 1d10 2d20 -2)")
    print("*" + " " * 21 + "Trait roll (Format: vigor -2)")
    print("*" + " " * 21 + "Reroll with a benny (Format: benny)")
    print("*" + " " * 21 + "Roll for initiative (Format: init)")
    print("*" + " " * 21 + "Roll for damage (Format: dmg 1d4 -2)")
    print("*" + " " * 21 + "Shaken status (Format: shaken)")
    print("*" + " " * 21 + "Take a fatigue (Format: fatigue)")
    print("*" + " " * 21 + "Take a wound (Format: wound)")
    print("*" + " " * 21 + "Heal from wound (Format: heal)")
    print("*" + " " * 21 + "Rest from fatigue (Format: rest)")
    print("*" + " " * 21 + "Exit this program (Format: exit)")
    print("*" + " " * 21 + "Update character sheet (Format: update)")
    print("*" * 65)


def intro_banner_voice():
    """
    # Purpose: Does all speech to text
    # Pre: None
    # Post: Outputs audio
    """

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')  # getting details of current voice
    engine.setProperty('voice', voices[1].id)  # changing index, changes voices. 1 for female
    rate = engine.getProperty('rate')  # getting details of current speaking rate
    engine.setProperty('rate', 125)  # setting up new voice rate
    engine.say("Hello, " + current_player.name)
    engine.say("I am your RPG assistant.")
    engine.say("I hope you have fun in tonight's session.")
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
    voice_thread = threading.Thread(target=intro_banner_voice)
    voice_thread.start()
    time.sleep(.25)
    print("*" * 65)
    print("* ", end='')
    for letter in "Hello," + " " + current_player.name:
        print(letter, end='', flush=True)
        time.sleep(.1)
    print("")
    print("* ", end='')
    time.sleep(1)
    for letter in "I am your RPG assistant.":
        print(letter, end='', flush=True)
        time.sleep(.1)
    print("")
    print("* ", end='')
    time.sleep(1)
    for letter in "I hope you have fun in tonight's session.":
        print(letter, end='', flush=True)
        time.sleep(.06)
    print("")
    print("*" * 65)
    print("* ", end="")
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


def sanitize_user_input(command):
    """
    # Purpose: Takes the raw user input and checks to see if valid
    # Pre: None
    # Post: Outputs a True if command is valid and False if not
    """
    # TODO need to change to allow for "dmg trait dice mod" works but "trait dice mod" does not work
    print("DEBUG::command" + str(command))
    follows_rules = True
    # need to change regular expressions to only allow accepted dice
    dice_regular_expression = re.compile(r"([1-9]|[1-9][0-9])d([2-9]|[1-9][0-9])")
    modifier_regular_expression = re.compile(r"[+-]\d{1,3}")
    possible_options = traits_ls + ["benny", "exit", "wound", "shaken", "init", "dmg", "soak", "heal", "exit",
                                    "fatigue", "rest", "update"]
    break_up_command = command.split(' ')
    # FIXME need to check for unique occurence of modifeirs and traits
    for option in break_up_command:
        if option not in possible_options and not dice_regular_expression.fullmatch(
                option) and not modifier_regular_expression.fullmatch(option):
            follows_rules = False
        if option in possible_options and break_up_command.count(option) > 1:
            follows_rules = False
        if modifier_regular_expression.fullmatch(option) and break_up_command.count(option) > 1:
            follows_rules = False
    return follows_rules

def update_character_sheets():
    """
    # Purpose:
    # Pre:
    # Post:
    """

    ftp = FTP('')
    ftp.connect('localhost', 1026)
    ftp.login()
    list_of_files = ftp.nlst()

    for character in list_of_files:
        with open("characters/" + character, 'wb') as file:
            ftp.retrbinary('RETR ' + character, file.write, 1024)
    ftp.quit()

# Main Start of Program
if __name__ == '__main__':
    # sets window size of terminal
    cmd = 'mode 66,40'
    os.system(cmd)
    current_player = player.player()
    all_dice = dice.dice()
    # list of all the traits and skills
    traits_ls = ['agility', 'smarts', 'spirit', 'strength', 'vigor', 'athletics', 'battle', 'boating',
                 'common_knowledge', 'driving', 'electronics', 'faith', 'fighting', 'focus', 'gambling', 'hacking',
                 'healing', 'intimidation', 'language', 'notice', 'occult', 'performance', 'persuasion', 'piloting',
                 'psionics', 'repair', 'research', 'riding', 'science', 'shooting',
                 'spellcasting', 'stealth', 'survival', 'taunt', 'thievery', 'weird_science']
    #update_character_sheets()
    # intro_banner()
    while True:
        main_menu()
        dice_roll = input("* Input: ").lower()
        # had to add a check for options with a space in them
        if "weird science" in dice_roll:
            dice_roll = dice_roll.replace("weird science", "weird_science")
        if "common knowledge" in dice_roll:
            dice_roll = dice_roll.replace("common knowledge", "weird_science")
        # if user input is not valid ignore rest of main program
        if not sanitize_user_input(dice_roll):
            print("* Unrecognized Command.")
            print("*" * 65)
        else:
            print("*" * 65)
            print("DEBUG::main_menu::" + str(dice_roll))
            # TODO damage for melee weapons includes trait dice
            # For rolling initiative
            # Roll a d20 for init with no modifier and no default d6
            if dice_roll == "init":
                all_dice.pick_your_poison("init", current_player)

            # For rolling traits, first elif statemnts is traits you have and second is traits you do not have
            elif any(elem in dice_roll.split(' ') for elem in current_player.traits.keys()):
                selected_trait = dice_roll.split(' ')[0]
                dice_roll = dice_roll.replace(selected_trait, current_player.traits[selected_trait])
                parse_down(dice_roll, all_dice)
                all_dice.pick_your_poison("traits", current_player)
            elif any(elem in dice_roll.split(' ') for elem in traits_ls):
                selected_trait = dice_roll.split(' ')[0]
                dice_roll = dice_roll.replace(selected_trait, '1d4 -2')
                parse_down(dice_roll, all_dice)
                all_dice.pick_your_poison("other_traits", current_player)

            # For rolling damage
            elif "dmg" in dice_roll:
                dice_roll = dice_roll.replace("dmg", '')
                parse_down(dice_roll, all_dice)
                all_dice.pick_your_poison("dmg", current_player)

            # For rerolling using bennies
            # FIXME: need a way to increase bennies
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
                    # You die if you crit fail in incapacitated
                    if all_dice.last_roll_was_crit_fail:
                        death_banner()
                        current_player.dead = True
                    if all_dice.last_actual_roll >= 4:
                        current_player.incap = False
                # FIXME: I don't think the if statement below needs to be here
                if current_player.wound_count >= 3:
                    current_player.wound_count = 3
                else:
                    current_player.wound_count += 1

            # For shaken status
            # If shaken you will stay in loop until you beat a spirit roll of 4 or pay a benny
            elif dice_roll == "shaken":
                current_player.shaken = True
                while current_player.shaken:
                    # FIXME: could remove this main_menu() during shaken
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

            # For fatigue counting, incapacitation, and resting
            elif dice_roll == "fatigue":
                if current_player.fat_count == 2:
                    current_player.incap = True
                    current_player.fat_count = 3
                    while current_player.incap:
                        rest_input = input("* " + "You are incapacitated and need rest.")
                        if rest_input == "rest":
                            current_player.fat_count = 0
                            current_player.incap = False
                            print("* " + "You feel rested.")
                        else:
                            pass
                else:
                    current_player.fat_count += 1

            # To roll death banner
            elif dice_roll == "death":
                death_banner()

            # To exit game
            elif dice_roll == "exit":
                # TODO: Need to write settings and stuff back out to .ini file. prototype function in player class
                print("* " + "You played for ")
                current_player.time_to_quit()
                sys.exit()
            elif dice_roll == "update":
                os.system("player.ini")
            else:
                parse_down(dice_roll, all_dice)
                all_dice.roll_them_bones("custom_roll", current_player)
