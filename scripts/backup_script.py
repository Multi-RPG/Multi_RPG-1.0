#!/usr/bin/env python3
"""
The purpose of this script is to:
1. create a timestamped database backup file
2. upload backup database to google cloud
3. clear backups older than the defined days

PS: FOR FULL AUTOMATION, SCHEDULE THIS FILE TO RUN AUTOMATICALLY AT AN INTERVAL.
PS2: MAKE SURE TO CHANGE PATHS TO FULL FILE PATHS IF THIS IS AUTOMATED
"""

import sqlite3
import shutil
import time
import os
import sys
from google.cloud import storage


def sqlite3_backup(db_file, directory):
    '''Copy the database file and timestamp it'''

    if not os.path.isdir(directory):
        raise Exception("Backup directory not found: {}".format(directory))

    # prepend current date to name of database file to backup
    backup_file_name = str(time.strftime("%Y-%m-%d---%H-%M--")) + os.path.basename(db_file)
    backup_file = os.path.join(directory, backup_file_name)

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

    # upload the backup to google cloud
    print("\nUploading to google cloud bucket now...\n")
    try:
        google_cloud_upload(backup_file)
        print("Successfully uploaded to google cloud bucket!")
    except:
        print("Failed to upload to google cloud. Please view "
              "https://cloud.google.com/storage/docs/reference/libraries#client-libraries-install-"
              " to set it up yourself if you wish to have this feature.")



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

def google_cloud_upload(file_path):
    """Uploads a file to the bucket."""
    # Edit this line with your private key json file path
    #os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\jake\Documents\Python discord bot\\tokens\creds.json"
    storage_client = storage.Client()
    bucket = storage_client.get_bucket("multirpg")
    blob = bucket.blob(os.path.basename(file_path))
    blob.upload_from_filename(file_path)


if __name__ == "__main__":
    # change working directory to parent to simplify file paths
    os.chdir("..")
    
    # pass in parameters: database file to backup, and directory to place backup in
    sqlite3_backup("db_and_words\hangman.db", "db_and_words\db_backups")
    # pass in parameters: directory to clear old backups from
    clear_old_backups("db_and_words\db_backups")

    print("\nBackup maintenance complete.")