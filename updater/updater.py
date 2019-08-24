# Updater program that checks version and updates character sheet with the Throwing D's Server
import os
import configparser
import zipfile
from ftplib import FTP
from time import sleep

# TODO: In future, add an option to open up the dm tool or player tool

def update_character_sheets():
    """
    # Purpose:
    # Pre:
    # Post:
    """
    ftp.cwd('characters')
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

    # grab from ftp server
    with open("current_version.zip",'wb') as file:
        ftp.retrbinary('RETR ' + 'current_version.zip', file.write, 1024)
    # unzip the files
    with zipfile.ZipFile('current_version.zip','r') as zip_file:
        zip_file.extractall('.')
    os.remove("current_version.zip")

if __name__ == '__main__':
    cmd = 'mode 66,40'
    os.system(cmd)
    # login to ftp server
    ftp = FTP('')
    ftp.connect('localhost',1026)
    print("*"*65)
    print("* Checking Version")
    server_version_number = ftp.login().split(' ')[1]
    print("* Server version " + server_version_number)
    config_file = configparser.ConfigParser()
    config_file.read("updater_settings.ini")
    local_version_number = config_file['version']['version']
    print("* Your version " + local_version_number)
    os.chdir("../main")
    if local_version_number != server_version_number:
        print("* Your version is outdated.")
        print("* Updating game files.")
        update_game_files()
        print("* Done!")
        print("* Updating Character Sheets.")
        update_character_sheets()
        print("* Done!")
        config_file['version']['version'] = server_version_number
        with open('../updater/updater_settings.ini','w') as config_file_output:
            config_file.write(config_file_output)
    else:
        print("* Luckily, you do not have to update.")
        print("* Updating Character Sheets.")
        update_character_sheets()
        print("* Done!")
        pass
    ftp.quit()
    print("* Loading Throwing D\'s",end='')
    for x in range(0,3):
        print(".", end='',flush=True)
        sleep(1)
    print("")
    os.system('cls')
    os.system("main.exe")
