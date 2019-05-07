#!/usr/bin/env python3
'''
The purpose of this script is to:
1. create a timestamped database backup file
2. clear backups older than the defined days
'''

import sqlite3
import shutil
import time
import os
import sys


def sqlite3_backup(db_file, directory):
    ''' Copy the database file and timestamp it '''

    if not os.path.isdir(directory):
        raise Exception("Backup directory not found: {}".format(directory))

    backup_file = os.path.join(directory, os.path.basename(db_file) + time.strftime("-%Y-%m-%d---%H-%M"))

    # connect to database
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    # prepare to lock database
    locked = 0
    counter = 0
    while not locked:
        # attempt to lock database
        try:
            cursor.execute('begin immediate')
            locked = 1
        # if failed to lock database, wait 3 seconds and try again
        except:
            locked = 0
            counter += 1
            # if failed to lock database 50 times, abort backup
            if counter > 50:
                sys.exit(0)
            time.sleep(3)

    # copy database file
    shutil.copyfile(db_file, backup_file)
    print("\nCreating {} and storing in {}".format(backup_file, directory))
    # unlock database
    connection.rollback()


def clear_old_backups(backup_dir):
    ''' Delete old database backups that are older than num_days '''
    num_days = 5
    elapse_time = time.time() - num_days * 86400

    print("\n------------------------------")
    print("Deleting any backups older than " + str(num_days) + " days...")
    print("\n------------------------------")

    for filename in os.listdir(backup_dir):
        backup_file = os.path.join(backup_dir, filename)
        if os.path.isfile(backup_file):
            if os.stat(backup_file).st_ctime < elapse_time:
                os.remove(backup_file)
                print("Deleting {} now!".format(backup_file))


if __name__ == "__main__":
    sqlite3_backup("..\hangman.db", "..\db_backups")
    clear_old_backups(".")

    print("\nBackup maintenance complete.")