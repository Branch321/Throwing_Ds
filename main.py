# Throwing_Ds is a dice roller for table top games(mostly Savage Worlds)
# Written in Python 3.6
import random

#TODO: Add this to Discord for friends to use


# Purpose: Write a function to parse down the code
# Post: Returns a dictionary of dice options (key is # of sides on dice, value is number of rolls)
def parse_down(dice_list):

    #dice_list = ['1d5'] #DELETE AFTER DEBUG
    dice_dictionary = {}
    for each_dice in dice_list:
        split_dice = each_dice.split('d')
        dice_dictionary.update({split_dice[1] : split_dice[0]})
    return dice_dictionary

# Purpose: Randomizes the dice rolls and prints the max of the rolls
#TODO: Add in -+ modifier rolls
#TODO: Deal with explosions

def random_dice_generator(dice_dictionary):
    print(dice_dictionary)
    actual_rolls = []
    for dice in dice_dictionary.keys():
        for number in range(0,int(dice_dictionary[dice])):
            actual_rolls.append(random.randint(1,int(dice)))
    print(actual_rolls)
    print(max(actual_rolls))

while True:
    #TODO: Add stat/skill specific rolls
    #Get input from user
    dice_roll = input("How many to roll? (format: 1d10 or initiative)  ")

    #Below is the initiative roll (Always 1d20)
    if dice_roll == "init":
        print(random.randint(1,20))
    #All other dice rolls
    else:
        dice_roll = dice_roll.split(' ')
        dice_options = parse_down(dice_roll)
        random_dice_generator(dice_options)

