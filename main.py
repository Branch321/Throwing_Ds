# Throwing_Ds is a dice roller for table top games(mostly Savage Worlds)
# Written in Python 3.6
import random
import copy
import time

#TODO: Add this to Discord for friends to use
#TODO: Add an ascii dice in the far future
#TODO: Need to add a verbosity flag for DEBUG:: messages
#TODO: Add better commenting
#TODO: Add a state for wounds, shaken/unshaken
#TODO: Create a class for player status

# Purpose: Function that parses and sanitizes user input
# Pre: damage variable determines whether to remove d6 for damage rolls
# Post: Returns a dictionary of dice options format: {# sided dice: # of rolls,'modifier':0}
def parse_down(dice_list,damage=False):
    dice_dictionary = {'modifier':0}
    #initilize dice_dictionary with 1d6 always because Savage Worlds specific dice roller
    if not damage:
        dice_dictionary['6'] = '1'
    #parse and form the dictionary to return
    for each_dice in dice_list:
        #condition for dice roll
        if 'd' in each_dice:
            split_dice = each_dice.split('d')
            dice_dictionary.update({split_dice[1]: split_dice[0]})
        #condition for modifier
        if '-' in each_dice or '+' in each_dice:
            dice_dictionary['modifier']=each_dice
            #dice_dictionary.update({'modifier': each_dice})
    return dice_dictionary

# Purpose: Randomizes the dice rolls and prints the max of the rolls
# Pre: must be passed a dictionary with the format {# sided dice: # of rolls,'modifier':0}
# Post: Prints to stdout
def random_dice_generator(dice_dictionary):
    global last_roll
    #Stores all rolls 
    actual_rolls = []
    #reads in the modifier roll
    last_roll = copy.deepcopy(dice_dictionary)
    modifier = dice_dictionary['modifier']
    #gets rid of the modifier in dictionary because it is no longer needed
    del dice_dictionary['modifier']
    for dice in dice_dictionary.keys():
        for number in range(0,int(dice_dictionary[dice][0])):
            current_roll = random.randint(1,int(dice))
            while current_roll == int(dice):
                print("There has been an explosion!")
                current_roll = current_roll+random.randint(1,int(dice)) 
            actual_rolls.append(current_roll)
    final_roll = max(actual_rolls)
    #below deals with crit fail roll
    #FIXME: if crit roll you do not need to output a 1
    if final_roll == 1:
        random_quote_index = random.randint(0, len(crit_quote_list))
        print(crit_quote_list[random_quote_index])
    #apply modifier
    final_roll_with_modifier = final_roll+int(modifier)
    #if the dice is below 1 set to 1
    if final_roll_with_modifier<1:
        final_roll_with_modifier=1
    print("* " + "Dice Roll is " + str(final_roll_with_modifier) + ".")

# Purpose: Prints out a menu with player status, last roll, and types of commands
# Pre: None
# Post: Will print to standard output
def main_menu():
    print("*"*65)
    print("*" + " Status: " + "Bennies: " + str(benny_counter))
    #FIXME: Need to make the "Last Roll" option look prettier
    print("*" + " Last Roll: " + str(last_roll))
    print("*" + " Types of Commands: Roll a dice (Format: 1d10 2d20 -2)")
    print("*"+" "*20+"Attribute roll (Format: vigor -2)")
    print("*"+" "*20+"Reroll with a benny (Format: benny)")
    print("*"+" "*20+"Roll for initiative (Format: init)")
    print("*"+" "*20+"Roll for damage (Format: damage 1d4 -2)")
    print("*"+" "*20+"Shaken status (Format: shaken)")
    print("*"+" "*20+"Exit this program (Format: exit)")
    print("*"*65)

# Purpose: Welcome banner for startup
# Pre: None
# Post: Will print to standard output
def intro_banner():
    print("*"*65)
    print("* ",end='')
    for letter in "Hello,":
        print(letter,end='',flush=True)
        time.sleep(.3)
    print("")
    print("* ",end='')
    time.sleep(1)
    for letter in "I am your Savage Worlds Assistant.":
        print(letter,end='',flush=True)
        time.sleep(.1)
    print("")
    print("* ",end='')
    for letter in "I hope you have fun in tonight's session.":
        print(letter, end='',flush=True)
        time.sleep(.1)
    print("")
    print("*"*65)
    time.sleep(1)

#need to do flags for DEBUG
#need to read in explosion quotes files into memory

#global variables and settings/configuration
last_roll = {}
benny_counter = 3

with open("crit_fail_quotes.txt") as file:
    #TODO: need to remove extra newline character off this list preferably with list comprehension or the like
    crit_quote_list = file.readlines()

#Start of program
intro_banner()
while True:
    #TODO: when adding shaken/unshaken your spirit roll has to beat a 4
    main_menu()
    #TODO: Add skill to options(only have attributes right now)
    options = {'agility':'1d8','smarts':'1d10','spirit':'1d4','strength':'1d6','vigor':'1d4'}
    dice_roll = input("* Input: ")
    print("*"*65)
    #Roll a d20 for init with no modifier
    if dice_roll == "init":
        print("* Your initiation roll is " + str(random.randint(1,20))+'.')
    #If shaken you will stay in loop until you beat a spirit roll of 4
    elif dice_roll == "shaken":
        shaken = True
        while shaken:
            input("* You are shaken. Hit enter to roll a spirit.")
            #FIXME: Need to fix the random_dice_generator() function to return a dice roll in order to use this
            shaken = False
    #Rolls a damage roll with modifier, does not roll a default 1d6
    elif dice_roll == "benny":
        if benny_counter==0:
            print("No more bennies")
        else:
            benny_counter-=1
            random_dice_generator(last_roll)
    elif "damage" in dice_roll:
        dice_roll = dice_roll.split(' ')
        del dice_roll[0]
        dice_options = parse_down(dice_roll,True)
        random_dice_generator(dice_options)
    #Rolls an attribute roll with modifier based on the options dictionary
    elif dice_roll in options.keys():
        dice_roll = options[dice_roll]
        dice_roll = dice_roll.split(' ')
        dice_options = parse_down(dice_roll)
        random_dice_generator(dice_options)
    #Exit condition
    elif dice_roll =="exit":
        exit()
    #All standard dice rolls
    else:
        dice_roll = dice_roll.split(' ')
        dice_options = parse_down(dice_roll)
        random_dice_generator(dice_options)

