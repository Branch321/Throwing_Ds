# Throwing_Ds is a dice roller for table top games(mostly Savage Worlds)
# Written in Python 3.6
import random

#TODO: Add in -+ modifier rolls
#TODO: Add in initiative rolls

# Purpose: Write a function to parse down the code
# Post: Returns a dictonary of dice options (key is # of sides on dice, value is number of rolls)
def parse_down(dice_list):

    #dice_list = ['1d5'] #DELETE AFTER DEBUG
    dice_dictionary = {}
    for each_dice in dice_list:
        split_dice = each_dice.split('d')
        dice_dictionary.update({split_dice[1] : split_dice[0]})
    return dice_dictionary

# Purpose: Randomizes the dice rolls and prints the max of the rolls
def random_dice_generator(dice_dictionary):
    print(dice_dictionary)
    actual_rolls = []
    for dice in dice_dictionary.keys():
        for number in range(0,int(dice_dictionary[dice])):
            actual_rolls.append(random.randint(1,int(dice)))
    print(actual_rolls)
    print(max(actual_rolls))

while True:
    dice_roll = input("How many to roll? (format: 1d10)      ")
    dice_roll = dice_roll.split(' ')
    dice_options = parse_down(dice_roll)
    random_dice_generator(dice_options)

