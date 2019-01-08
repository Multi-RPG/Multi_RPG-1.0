#!/usr/bin/env python3
import configparser
import sys
import random
import discord
from Users import Users
from Database import Database
from discord.ext import commands
from pathlib import Path
from datetime import date

# IMPORTANT: FOR FULL AUTOMATION, SCHEDULE THIS SCRIPT TO RUN AUTOMATICALLY AT AN INTERVAL.
#   EX: CRONTAB WITH DAILY EXECUTION AT 8AM. HOWEVER, MAKE SURE TO CHANGE PATH TO YOUR FULL FILE PATH FOR BOT_TOKEN_PATH

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
    print("\n","Discord bot token not found at: ",bot_token_path,"... Please correct file path in daily_maintenance.py file.")
    sys.exit()

@client.event
async def on_ready():
    print('Logged in as\n'
          + client.user.name + '\n'
          + client.user.id + '\n'
          + '---------')

    # generate a random winning number 1-5
    win_number = random.randint(1,5)
    # open database
    db = Database(0)
    db.connect()
    # get python list of winner ticket id's who match today's winning number
    std_winners, prem_winners = db.get_lottery_winners(win_number)
    std_winners_string = ''
    for winner in std_winners:
        # create instance of each basic ticket user who won, and update their money
        user = Users(winner)
        user.update_user_money(250)
        # alter each item on list to discord @ format and concatenate into 1 string to ping winners below
        std_winners_string += ('**TICKET ID:** ' + winner + ' <@' + winner + '>\n')
        
    prem_winners_string = ''
    for winner in prem_winners:
        # create instance of each premium ticket user who won, and update their
        user = Users(winner)
        user.update_user_money(1000)
        # alter each item on list to discord @ format and concatenate into 1 string to ping winners below
        prem_winners_string += ('**TICKET ID:** ' + winner + ' <@' + winner + '>\n')
    

    # for each server the bot is in, post the lottery results in the lottery channel
    for server in client.servers:
        # create boolean for each server, to dictate whether or not the 'lottery' channel was located
        channel_found = 0

        while channel_found == 0:
            for channel in server.channels:
                if channel.name == 'lottery':
                    channel_found = 1
                    if std_winners or prem_winners:
                        await client.send_message(channel, "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁\n"
                                                           + "<a:worrycash:525200274340577290>**  LOTTERY ANNOUNCEMENT**"
                                                           + "  <a:worrycash:525200274340577290> _" + str(date.today()) + "_"
                                                           + "\nToday's winning number is... **"
                                                           + str(win_number) + "**\nThe lucky **$250** winners: \n"
                                                           + std_winners_string + "\nThe lucky premium **$1,000** winners: \n"
                                                           + prem_winners_string + "\n\nDaily shop has been reset! Check **=shop**!"
                                                           + "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁\n")
                    elif not std_winners or prem_winners:
                        std_winners_string = '<a:worrycry:525209793405648896> **No winners today**... <a:worrycry:525209793405648896>'
                        await client.send_message(channel, "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁\n"
                                                           + "<a:worrycash:525200274340577290>**  LOTTERY ANNOUNCEMENT**"
                                                           + "  <a:worrycash:525200274340577290> _" + str(date.today()) + "_"
                                                           + "\nToday's winning number is... **"
                                                           + str( win_number) + "**\nThe lucky winners: \n"
                                                           + std_winners_string + "\n\nDaily shop has been reset! Check **=shop**!"
                                                           + "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁\n")

            # if there were no channels found with the name 'lottery'.....
            # make the channel, then restart the loop to iterate through the channels and send results in the new channel
            if channel_found == 0:
                try:
                    await client.create_channel(server, 'lottery', type=discord.ChannelType.text)
                except:
                    # if the bot failed to make the channel, simply move on and assume the channel exists
                    channel_found = 1


    # RESET DAILY SHOP NOW! 
    db.reset_shop()

    # make sure to change this path to the full file path if you plan to use crontab, or else it will not work
    config = configparser.ConfigParser()
    items_path = Path("db_and_words/all_items.ini")  # use forward slash "/" for path directories
    if items_path.is_file():
        config.read(items_path)
    else:
        print("\n", "User tokens not found at: ", items_path, "... Please correct file path in Dibs.py file.")
        sys.exit()

    # parse through each section in the items in the .ini file
    # each item has a 12% chance to be inserted into the daily shop
    for item in config.sections():
        if 12 >= random.randint(1, 100) >= 1:
            item_name = config.get(item, 'name')
            item_type = config.get(item, 'type')
            item_level = config.get(item, 'level')
            item_price = config.get(item, 'price')

            db.insert_shop_item(item_name, item_type, item_level, item_price)
    

    sys.exit(0)
client.run(TOKEN)
