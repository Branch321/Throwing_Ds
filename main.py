# Throwing_Ds is a dice roller for table top games(mostly Savage Worlds)
# Written in Python 3.6
import random

#TODO: Add this to Discord for friends to use
#      Need to fully redo how modifiers works in this program

# Purpose: Function that parses and sanitizes user input
# Post: Returns a dictionary of dice options format: {# sided dice: [# of rolls, modifier]}
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
            #TODO: Deal with explosions here
            current_roll = random.randint(1,int(dice))
            actual_rolls.append(current_roll)
    print(actual_rolls)
    print(max(actual_rolls))

while True:
    #TODO: Add stat/skill specific rolls
    #Get input from user
    dice_roll = input("How many to roll? (format: 1d10-2 or init)  ")
    #Below is the initiative roll (Always 1d20)
    if dice_roll == "init":
        print(random.randint(1,20))
    #All other dice rolls
    else:
        dice_roll = dice_roll.split(' ')
        dice_options = parse_down(dice_roll)
        random_dice_generator(dice_options)

