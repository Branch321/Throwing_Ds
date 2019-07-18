# Throwing_Ds is a dice roller for table top games(mostly Savage Worlds)
# Written in Python 3.6
import random

#TODO: Add this to Discord for friends to use
#TODO: Instead of using for loops with .append we need to use  newlist = map(myfunc, oldlist) for speed
#TODO: Add an ascii dice in the far future
#TODO: Need to add a verbosity flag for DEBUG:: messages

# Purpose: Function that parses and sanitizes user input
# Pre: damage variable determines whether to remove d6 for damage rolls
# Post: Returns a dictionary of dice options format: {# sided dice: # of rolls,'modifier':0}
def parse_down(dice_list,damage=False):
    dice_dictionary = {'modifier':0}
    #initilize dice_dictionary with 1d6 always because Savage Worlds specific dice roller
    if not damage:
        dice_dictionary = {'6':'1'}
    for each_dice in dice_list:
        if 'd' in each_dice:
            split_dice = each_dice.split('d')
            dice_dictionary.update({split_dice[1]: split_dice[0]})
        if '-' in each_dice or '+' in each_dice:
            dice_dictionary.update({'modifier': each_dice})
    return dice_dictionary

# Purpose: Randomizes the dice rolls and prints the max of the rolls
def random_dice_generator(dice_dictionary):
    actual_rolls = []
    modifier = dice_dictionary['modifier']
    del dice_dictionary['modifier']
    for dice in dice_dictionary.keys():
        for number in range(0,int(dice_dictionary[dice][0])):
            current_roll = random.randint(1,int(dice))
            #TODO: Need to verify this actually works
            while current_roll == int(dice):
                print("There has been an explosion!")
                current_roll = current_roll+random.randint(1,int(dice)) 
            actual_rolls.append(current_roll)
            #TODO: add a crit fail option here
    print(max(actual_rolls)+int(modifier))

while True:
    #TODO: Add skill to options(only have attributes right now)
    options = {'agility':'1d8','smarts':'1d10','spirit':'1d4','strength':'1d6','vigor':'1d4'}
    #TODO: need to add a bigger text menu with all options
    dice_roll = input("How many to roll? (format: 1d10 -2, init, attribute (lowercase))  ")
    #Below is the initiative roll (Always 1d20)
    if dice_roll == "init":
        print(random.randint(1,20))
    elif "damage" in dice_roll:
        dice_roll = dice_roll.split(' ')
        del dice_roll[0]
        dice_options = parse_down(dice_roll,True)
        random_dice_generator(dice_options)
    elif dice_roll in options.keys():
        dice_roll = options[dice_roll]
        dice_roll = dice_roll.split(' ')
        dice_options = parse_down(dice_roll)
        random_dice_generator(dice_options)
    elif dice_roll =="exit":
        exit()
    else:
        dice_roll = dice_roll.split(' ')
        dice_options = parse_down(dice_roll)
        random_dice_generator(dice_options)

