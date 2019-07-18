# Throwing_Ds is a dice roller for table top games(mostly Savage Worlds)
# Written in Python 3.6
import random

#TODO: Add this to Discord for friends to use
#TODO: Instead of using for loops with .append we need to use  newlist = map(myfunc, oldlist) for speed

# Purpose: Function that parses and sanitizes user input
# Post: Returns a dictionary of dice options format: {# sided dice: # of rolls,'modifier':0}
def parse_down(dice_list):
    #initilize dice_dictionary with 1d6 always because Savage Worlds specific dice roller
    #TODO: Need to not roll a default d6 on damage rolls
    dice_dictionary = {'6':'1','modifier':'0'}
    for each_dice in dice_list:
        if 'd' in each_dice:
            split_dice = each_dice.split('d')
            dice_dictionary.update({split_dice[1]: split_dice[0]})
        if '-' in each_dice or '+' in each_dice:
            dice_dictionary.update({'modifier': each_dice})
    print(dice_dictionary)
    return dice_dictionary

# Purpose: Randomizes the dice rolls and prints the max of the rolls
def random_dice_generator(dice_dictionary):
    print(dice_dictionary)
    actual_rolls = []
    modifier = dice_dictionary['modifier']
    del dice_dictionary['modifier']
    for dice in dice_dictionary.keys():
        for number in range(0,int(dice_dictionary[dice][0])):
            current_roll = random.randint(1,int(dice))
            #TODO: Need to verify this actually works
#            print("DEBUG::current_roll " + str(current_roll))
#            print("DEBUG::dice " + str(dice))
            while current_roll == int(dice):
                print("There has been an explosion!")
                current_roll = current_roll+random.randint(1,int(dice))
#                print("DEBUG::current_roll " + str(current_roll))
            actual_rolls.append(current_roll)
            #TODO: add a crit roll option here
    print(actual_rolls)
    print(max(actual_rolls)-int(modifier))
#TODO: Need to add an option to "Exit" this loop
while True:
    #TODO: Add skill to options(only have attributes right now)
    options = {'agility':'1d8','smarts':'1d10','spirit':'1d4','strength':'1d6','vigor':'1d4'}
    #Get input from user
    dice_roll = input("How many to roll? (format: 1d10 -2, init, or attribute (lowercase))  ")
    #Below is the initiative roll (Always 1d20)
    print("DEBUG:: " + str(dice_roll))
    if dice_roll == "init":
        print(random.randint(1,20))
    elif dice_roll in options.keys():
        #TODO: Need to add modifiers to attribute rolls
        #FIXME: Not parsing the attribute correctly
        print("DEBUG:: " + str(options[dice_roll]))
        dice_roll = options[dice_roll]
        dice_roll = dice_roll.split(' ')
        dice_options = parse_down(dice_roll)
        #print(dice_options)
        random_dice_generator(dice_options)
    #All other dice rolls
    else:
        print("DEBUG:: " + "Did I make it this far?")
        dice_roll = dice_roll.split(' ')
        dice_options = parse_down(dice_roll)
        random_dice_generator(dice_options)

