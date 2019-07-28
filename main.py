# Throwing_Ds is a dice roller for table top games(mostly Savage Worlds)
# Written in Python 3.6.1
# External Libraries Needed: Text-to-Speech - pyttsx3 2.71 - https://github.com/nateshmbhat/pyttsx3

import os
import re
import sys
import threading
import time
from ftplib import FTP
import logging

import pyttsx3

import dice
import player


# TODO: Add this to Discord for friends to use
# TODO: Check for luck and great luck edges
# TODO: Add an ascii dice in the far future
# TODO: Need to add a verbosity flag for DEBUG:: messages
# TODO: Add better commenting
# TODO: Added a dice statistics option to print out all the statistics of the current session
# FIXME: need to do a dice_roll.split() in the main program because it is the first thing we call in parse_down() and sanitize_user_input()
# TODO: add a full option list in main function for user_input
# FIXME: rest causes the program to crash
# TODO: finish logging abilities
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

def pick_your_character():
    user_character_input = ""
    list_of_characters = os.listdir("characters/")
    list_of_characters_without_file_format = [elem[:-4] for elem in list_of_characters]
    print("*"*65)
    print("* Character List: ")
    print("* ---------------")
    for character in list_of_characters_without_file_format:
        print("* " + character)
    print("*")
    #FIXME get rid of the line below this on release
    user_character_input = "Toskurr"
    while user_character_input not in list_of_characters_without_file_format:
        user_character_input = input("* Which character would you like to play? ")
    return user_character_input

def intro_banner():
    """
    # Purpose: Welcome banner for startup
    # Pre: None
    # Post: Will print to standard output
    """
    # TODO: change how this works using callbacks so the prints happen with the voice
    # Below is sample code for text to voice
    voice_thread = threading.Thread(target=intro_banner_voice)
    voice_thread.start()
    time.sleep(.25)
    print("*" * 65)
    print("* ", end='')
    for letter in "Hello " + " " + current_player.name + ",":
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
    print("Updating your character sheets now", end='')
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
    follows_rules = True
    # need to change regular expressions to only allow accepted dice
    dice_regular_expression = re.compile(r"([1-9]|[1-9][0-9])d([2-9]|[1-9][0-9])")
    modifier_regular_expression = re.compile(r"[+-]\d{1,3}")
    possible_options = traits_ls + ["benny", "exit", "wound", "shaken", "init", "dmg", "soak", "heal", "exit",
                                    "fatigue", "rest", "update", "benny+"]
    break_up_command = command.split(' ')
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


def dmg_menu():
    os.system("cls")
    print("*"*65)
    print("* Weapons List:")
    print("* ---------------")
    list_to_choose_from = list(enumerate(current_player.weapons_dictionary.keys(),start=1))
    for weapon in list_to_choose_from:
        print("* " + str(weapon[0]) +") "+  weapon[1])
    dmg_menu_user_input = input("* Type in number of weapon or custom roll. ")
    dmg_menu_user_input = current_player.weapons_dictionary[list_to_choose_from[int(dmg_menu_user_input)-1][1]].replace("+"," ")
    print("Is input good? " + str(sanitize_user_input(dmg_menu_user_input)))
    #TODO: finish dmg_menu


# Main Start of Program
if __name__ == '__main__':
    # sets window size of terminal
    cmd = 'mode 66,40'
    os.system(cmd)
    logging.basicConfig(filename='logfile.log', level=logging.DEBUG)

    chosen_character = pick_your_character()
    logging.debug('pick_your_character() has finished.')
    current_player = player.player(chosen_character)
    logging.debug('player.player() initiated.')
    all_dice = dice.dice()
    logging.debug('dice.dice() initiated.')
    #intro_banner()
    logging.debug('intro_banner has finished.')
    # list of all the traits and skills
    traits_ls = ['agility', 'smarts', 'spirit', 'strength', 'vigor', 'athletics', 'battle', 'boating',
                 'common_knowledge', 'driving', 'electronics', 'faith', 'fighting', 'focus', 'gambling', 'hacking',
                 'healing', 'intimidation', 'language', 'notice', 'occult', 'performance', 'persuasion', 'piloting',
                 'psionics', 'repair', 'research', 'riding', 'science', 'shooting',
                 'spellcasting', 'stealth', 'survival', 'taunt', 'thievery', 'weird_science']
    #update_character_sheets()
    logging.debug('update_character_sheets() has finished')
    while True:
        main_menu()
        dice_roll = input("* Input: ").lower()
        logging.debug("User has picked::%s",dice_roll)
        # had to add a check for options with a space in them
        if "weird science" in dice_roll:
            dice_roll = dice_roll.replace("weird science", "weird_science")
        if "common knowledge" in dice_roll:
            dice_roll = dice_roll.replace("common knowledge", "weird_science")
        # if user input is not valid ignore rest of main program
        if not sanitize_user_input(dice_roll):
            logging.debug("User option did not make it past sanitize_user_input()")
            print("* Unrecognized Command.")
            print("*" * 65)
        else:
            logging.debug("User option did make it past sanitize_user_input()")
            print("*" * 65)
            # For rolling initiative
            # Roll a d20 for init with no modifier and no default d6
            if dice_roll == "init":
                logging.debug("User option switched into init")
                all_dice.pick_your_poison("init", current_player)

            # For rolling damage
            elif "dmg" in dice_roll:
                logging.debug("User option switched into dmg")
                #dice_roll = dice_roll.replace("dmg", '')
                #parse_down(dice_roll, all_dice)
                #all_dice.pick_your_poison("dmg", current_player)
                dmg_menu()
            # For rolling traits, first elif statemnts is traits you have and second is traits you do not have
            elif any(elem in dice_roll.split(' ') for elem in current_player.traits.keys()):
                logging.debug("User option switched into a trait roll.")
                selected_trait = dice_roll.split(' ')[0]
                dice_roll = dice_roll.replace(selected_trait, current_player.traits[selected_trait])
                parse_down(dice_roll, all_dice)
                all_dice.pick_your_poison("traits", current_player)
            elif any(elem in dice_roll.split(' ') for elem in traits_ls):
                logging.debug("User option switched into a unowned trait roll.")
                selected_trait = dice_roll.split(' ')[0]
                dice_roll = dice_roll.replace(selected_trait, '1d4 -2')
                parse_down(dice_roll, all_dice)
                all_dice.pick_your_poison("other_traits", current_player)

            # For rerolling using bennies
            elif dice_roll == "benny":
                logging.debug("User option switched into a benny")
                if current_player.benny_counter == 0:
                    print("No more bennies.")
                elif not all_dice.last_roll:
                    print("Why would you try to benny when you haven't rolled a single die yet.")
                elif all_dice.last_roll_was_crit_fail:
                    print("* You cannot benny if you crit failed last roll.")
                else:
                    current_player.benny_counter -= 1
                    all_dice.pick_your_poison("benny", current_player)

            # For wounds and incapacitation
            # If incapacitated you will stay in loop until you beat a vigor roll of 4
            elif dice_roll == "wound":
                logging.debug("User option switched into a wound.")
                if current_player.wound_count == 3:
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
                        current_player.wound_count = 3
                else:
                    current_player.wound_count += 1

            # For shaken status
            # If shaken you will stay in loop until you beat a spirit roll of 4 or pay a benny
            elif dice_roll == "shaken":
                logging.debug("User option has switched into shaken.")
                current_player.shaken = True
                while current_player.shaken:
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
                logging.debug("User option has switched into soak.")
                dice_roll = current_player.traits['vigor']
                parse_down(dice_roll, all_dice)
                all_dice.pick_your_poison("soak", current_player)

            # For healing wounds
            elif dice_roll == "heal":
                logging.debug("User option has switched into heal.")
                if current_player.wound_count > 0:
                    current_player.wound_count -= 1
                    print("* " + "One of your wounds has been healed.")
                else:
                    print("* " + "You do not have any wounds to heal.")

            # For fatigue counting, incapacitation, and resting
            elif dice_roll == "fatigue":
                logging.debug("User option has switched into fatigue.")
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
                    current_player.fat_count += 1

            elif dice_roll == "rest":
                if current_player.fat_count > 0:
                    current_player.fat_count = 0
                    print ("Your feel rested.")
                else:
                    print("You do not need rest.")

            elif dice_roll == "benny+":
                current_player.benny_counter += 1

            # To roll death banner
            elif dice_roll == "death":
                death_banner()

            # To exit game
            elif dice_roll == "exit":
                logging.debug("User option has switched into exit.")
                # TODO: Need to write settings and stuff back out to .ini file. prototype function in player class
                print("* " + "You played for ")
                current_player.time_to_quit()
                sys.exit()
            elif dice_roll == "update":
                logging.debug("User option has switched into update.")
                os.system("player.ini")
            else:
                logging.debug("User option has switched into a custom roll.")
                parse_down(dice_roll, all_dice)
                all_dice.roll_them_bones("custom_roll", current_player)
