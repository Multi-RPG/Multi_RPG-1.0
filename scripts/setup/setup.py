#!/usr/bin/env python3
"""
The purpose of this script is to:
1. extract setup files for the bot to function
2. build an empty database for the bot using an extracted schema
"""

import os
import sqlite3
import zipfile
import sys


def extract_directories():
    # extract zip with setup files
    zipper = zipfile.ZipFile('setup_files.zip', 'r')
    zipper.extractall('../..')
    zipper.close()


def create_database():
    # create database
    connection = sqlite3.connect('../../db_and_words/hangman.db')
    # open our database schema
    schema = open('../../db_and_words/schema.sql', 'r').read()
    # import the schema into the database
    connection.executescript(schema)


if __name__ == "__main__":
    # check if database file already exists
    if os.path.isfile('../../db_and_words/hangman.db'):
        # confirm if user wants to overwrite the database
        confirm = input("Database file already exists. Are you sure you want to continue with setup? Type yes or no:\n")
        # delete the current database if they do, and continue on
        if confirm.lower() == 'yes':
            os.remove('../../db_and_words/hangman.db')
        # exit script if they do not
        else:
            print("Setup cancelled!")
            sys.exit(0)

    # extract directories with setup files
    extract_directories()
    # create database from schema extracted
    create_database()
    print("Setup complete! Please continue to edit tokenbot.ini in the tokens folder.")
