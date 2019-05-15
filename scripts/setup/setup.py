#!/usr/bin/env python3
"""
The purpose of this script is to:
1. build the sqlite3 database for the bot
2. copy all startup files into main directory
"""

import os
import sqlite3
import shutil
import distutils.dir_util
import zipfile


def create_database():
    # create database
    connection = sqlite3.connect('db_and_words/hangman.db')
    # open our database schema
    schema = open('db_and_words/schema.sql', 'r').read()
    # import the schema into the database
    connection.executescript(schema)


def copy_directories():
    # extract zip with setup files
    zip = zipfile.ZipFile('setup_files.zip', 'r')
    zip.extractall('.')
    zip.close()

    create_database()

    # copy this directory into the main directory, 2 parent folders up
    distutils.dir_util.copy_tree('.', '..\..')

    # delete the extracted setup files
    shutil.rmtree('custom_memes')
    shutil.rmtree('db_and_words')
    shutil.rmtree('logs')
    shutil.rmtree('tokens')

    # delete the setup files that got copied
    os.remove('../../setup.py')
    os.remove('../../setup_files.zip')


if __name__ == "__main__":
    copy_directories()