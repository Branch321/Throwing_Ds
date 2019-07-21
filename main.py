# Throwing_Ds is a dice roller for table top games(mostly Savage Worlds)
# Written in Python 3.6
# External Libraries Needed: Text-to-Speech - pyttsx3 2.71 - https://github.com/nateshmbhat/pyttsx3

import sys
import time

import dice
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
# TODO Check for luck and great luck edges
# TODO: Add an ascii dice in the far future
# TODO: Need to add a verbosity flag for DEBUG:: messages
# TODO: Add better commenting
# TODO: Need to add a sanitization function to stop program from crashing on bad input
# TODO: Added a text to voice for introduction
# TODO: Added a dice statistics option to print out all the statistics of the current session
# TODO: Create a logger for all dice history

def parse_down(dice_list, all_dice):
    # TODO: Need to check if user input is valid dice
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
    # TODO: Need to multi-thread  the voice to test for the intro_banner function
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
if __name__ == '__main__':
    current_player = player.player()
    all_dice = dice.dice()

    # intro_banner()
    while True:
        main_menu()
        dice_roll = input("* Input: ")
        print("*" * 65)

        # TODO damage for melee weapons includes trait dice
        # Roll a d20 for init with no modifier and no default d6
        if dice_roll == "init":
            all_dice.pick_your_poison("init", current_player)
        elif any(elem in dice_roll.split(' ') for elem in current_player.traits.keys()):
            selected_trait = dice_roll.split(' ')[0]
            dice_roll = dice_roll.replace(selected_trait, current_player.traits[selected_trait])
            parse_down(dice_roll, all_dice)
            all_dice.pick_your_poison("traits", current_player)
        elif "dmg" in dice_roll:
            dice_roll = dice_roll.replace("dmg", '')
            parse_down(dice_roll, all_dice)
            all_dice.pick_your_poison("dmg", current_player)
            # wound modifier
        # Rerolls the last current_player.last_roll
        elif dice_roll == "benny":
            if current_player.benny_counter == 0:
                print("No more bennies")
            elif all_dice.last_roll_was_crit_fail:
                print("* You cannot benny if you crit failed last roll.")
            else:
                current_player.benny_counter -= 1
                all_dice.pick_your_poison("benny", current_player)
        elif dice_roll == "wound":
            # FIXME Incapacitation only triggers once before not triggering
            if current_player.wound_count >= 3:
                current_player.incap = True
                current_player.wound_count = 3
            # If incapacitated you will stay in loop until you beat a vigor roll of 4
            # FIXME Cannot get out of incap loop
            while current_player.incap:
                input("* You are incapacitated. Hit enter to roll a vigor.")
                dice_roll = current_player.traits['vigor']
                parse_down(dice_roll, all_dice)
                all_dice.pick_your_poison("traits", current_player)
                if all_dice.last_actual_roll == 1:
                    death_banner()
                    current_player.dead = True
                if all_dice.last_actual_roll >= 4:
                    current_player.incap = False
            else:
                current_player.wound_count += 1
            # This is for shaken status
        elif dice_roll == "shaken":
            current_player.shaken = True
            #FIXME Cannot unshake with spirit roll
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
                    parse_down(dice_roll, all_dice)
                    all_dice.pick_your_poison("traits", current_player)
                    if spirit_check_value >= 4:
                        current_player.shaken = False
        elif dice_roll == "soak":
                dice_roll = current_player.traits['vigor']
                parse_down(dice_roll, all_dice)
                all_dice.pick_your_poison("soak", current_player)
        elif dice_roll == "heal":
            if current_player.wound_count > 0:
                current_player.wound_count -=1
                print("One of your wounds has been healed.")
            else:
                print("You do not have any wounds to heal.")
        elif dice_roll == "fatigue":
            current_player.fat_count += 1
        elif dice_roll == "death":
            death_banner()
        elif dice_roll == "exit":
            # TODO: Need to write settings and stuff back out to .ini file. prototype function in player class
            print("* You played for ")
            sys.exit()
        else:
            parse_down(dice_roll, all_dice)
            all_dice.roll_them_bones("custom_roll", current_player)
