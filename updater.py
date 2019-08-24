# Updater program that checks version and updates character sheet with the Throwing D's Server
import os
from ftplib import FTP


# TODO: In future, add an option to open up the dm tool or player tool
def update_character_sheets():
    """
    # Purpose:
    # Pre:
    # Post:
    """
    list_of_files = ftp.nlst()
    for character in list_of_files:
        with open("characters/" + character, 'wb') as file:
            ftp.retrbinary('RETR ' + character, file.write, 1024)

def update_game_files():
    """
    # Purpose:
    # Pre:
    # Post:
    """
    pass

def intro_banner_updater():
    pass

if __name__ == '__main__':
    cmd = 'mode 66,40'
    os.system(cmd)


# login to ftp server
ftp = FTP('')
ftp.connect('localhost',1026)
ftp.login()


# check version number
# if not same version number: update all files including character sheets
# if same version number: update all character sheets

ftp.quit()
# run main/main.py
