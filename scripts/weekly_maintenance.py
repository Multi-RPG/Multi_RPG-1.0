#!/usr/bin/env python3
"""
The purpose of this script is to:
1. connect to database, and reset all "peace_cd" to 0 in "Users" table

PS: FOR FULL AUTOMATION, SCHEDULE THIS FILE TO RUN AUTOMATICALLY AT AN INTERVAL.
PS2: MAKE SURE TO CHANGE PATHS TO FULL FILE PATHS IF THIS IS AUTOMATED
"""

import configparser
import sys
import os
# add parent folder to module path. can comment this out if using virtual environment
sys.path.append('..')

from Database import Database
from discord.ext import commands
from pathlib import Path


# change working directory to parent to simplify file paths
os.chdir("..")

# startup discord client
client = commands.Bot(command_prefix=["=", "%"])

# set up parser to config through our .ini file with our bot's token
config = configparser.ConfigParser()
bot_token_path = Path("tokens/tokenbot.ini") # use forward slash "/" for path directories
# confirm the token is located in the above path
if bot_token_path.is_file():
    config.read(bot_token_path)
    # we now have the bot's token
    TOKEN = config.get('BOT1', 'token')
else:
    print("\n","Discord bot token not found at: ",bot_token_path,
          "... Please correct file path in weekly_maintenance.py file.")
    sys.exit()

@client.event
async def on_ready():
    print('Logged in as\n'
          + client.user.name + '\n'
          + client.user.id + '\n'
          + '---------')

    # open database
    db = Database(0)
    db.connect()

    """ PERFORM WEEKLY PEACE COOLDOWN RESET """
    db.reset_peace_cooldowns()

    # end this weekly maintenance program
    sys.exit(0)

client.run(TOKEN)
