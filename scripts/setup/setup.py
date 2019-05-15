#!/usr/bin/env python3
"""
The purpose of this script is to:
1. build the database for the bot
2. copy all startup files into main directory
"""

import os
import sqlite3
import zipfile
import sys


def copy_directories():
    # extract zip with setup files
    zip = zipfile.ZipFile('setup_files.zip', 'r')
    zip.extractall('../..')
    zip.close()

    # create database from schema extracted
    create_database()


def create_database():
    # check if database file already exists
    if os.path.isfile('../../db_and_words/hangman.db'):
        # confirm if user wants to overwrite the database
        confirm = input("Database file already exists. Are you sure you want to override it? Type yes or no:\n")
        # overwrite the database if they do, and continue on
        if confirm.lower() == 'yes':
            os.remove('../../db_and_words/hangman.db')
        # exit script if they do not
        else:
            sys.exit(0)

    # create database
    connection = sqlite3.connect('../../db_and_words/hangman.db')
    # open our database schema
    schema = open('../../db_and_words/schema.sql', 'r').read()
    # import the schema into the database
    connection.executescript(schema)


if __name__ == "__main__":
    copy_directories()
    print("Setup complete! Please continue to edit tokenbot.ini in the tokens folder.")
