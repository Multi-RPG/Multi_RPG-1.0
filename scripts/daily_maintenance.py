#!/usr/bin/env python3
"""
The purpose of this script is to:
1. reset and repopulate "Shops" table in database
2. choose a winning lottery number, reward winners, and reset "Lottery" table in database
3. determine tournament winners, reward winners, and reset "Battles" table in database

PS: FOR FULL AUTOMATION, SCHEDULE THIS FILE TO RUN AUTOMATICALLY AT AN INTERVAL.
PS2: MAKE SURE TO CHANGE PATHS TO FULL FILE PATHS IF THIS IS AUTOMATED
"""

import configparser
import sys
import random
import discord
import numpy
import os
# add parent folder to module path. can comment this out if using virtual environment
sys.path.append('..')

from numpy import random
from Users import Users
from Database import Database
from discord.ext import commands
from pathlib import Path
from datetime import date


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
    print("\n","Discord bot token not found at: ",bot_token_path,"... Please correct file path in daily_maintenance.py file.")
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

    """ PERFORM DAILY SHOP MAINTENANCE NOW! """
    db.reset_shop()

    # make sure to change this path to the full file path if you plan to use crontab, or else it will not work
    config = configparser.ConfigParser()
    items_path = Path("db_and_words/all_items.ini")  # use forward slash "/" for path directories
    if items_path.is_file():
        config.read(items_path)
    else:
        print("\n", "Shop items file not found at: ", items_path, "... Please correct file path in daily_maintenance.py file.")
        sys.exit()

    # parse through each section in the items in the .ini file
    # each item has a 17% chance to be inserted into the daily shop
    for item in config.sections():
        if 17 >= random.randint(1, 100) >= 1:
            item_name = config.get(item, 'name')
            item_type = config.get(item, 'type')
            item_level = config.get(item, 'level')
            item_price = config.get(item, 'price')

            db.insert_shop_item(item_name, item_type, item_level, item_price)

    """ PERFORM DAILY LOTTERY MAINTENANCE NOW """
    # generate a random winning number 1-5
    win_number = random.randint(1,5)
    # get python list of winner ticket id's who match today's winning number
    std_winners, prem_winners = db.get_lottery_winners(win_number)
    # we have today's winners now, so reset lottery
    db.reset_lottery()
    std_winners_string = ''
    for winner in std_winners:
        # create instance of each basic ticket user who won, and update their money
        user = Users(winner)
        user.update_user_money(user.get_user_level(0) * 100)
        # alter each item on list to discord @ format and concatenate into 1 string to ping winners below
        std_winners_string += ('\n**TICKET ID:** ' + winner + ' <@' + winner + '>')
        
    prem_winners_string = ''
    for winner in prem_winners:
        # create instance of each premium ticket user who won, and update their
        user = Users(winner)
        user.update_user_money(user.get_user_level(0) * 170)
        # alter each item on list to discord @ format and concatenate into 1 string to ping winners below
        prem_winners_string += ('\n**TICKET ID:** ' + winner + ' <@' + winner + '>')

    # prepare string of shop reset notifcation & lottery results to send to every discord server
    if not std_winners:
        std_winners_string = '\n<a:worrycry:525209793405648896> no basic winners...  <a:worrycry:525209793405648896>'
    if not prem_winners:
        prem_winners_string = '\n<a:worrycry:525209793405648896> no premium winners...  <a:worrycry:525209793405648896>'

    # split shop & lottery announcements into 2 strings
    # have to insert encode \u200B for spaces when using discord encoding
    global_announcement1 = "__**SHOP ANNOUNCEMENT**__ \u200B \u200B" \
                           + "_" + str(date.today()) + "_" \
                           + "\n:shopping_cart: \u200B Daily shop just reset... Check out **=shop**!\n"
    global_announcement2 = "__**LOTTERY ANNOUNCEMENT**__ \u200B \u200B_" + str(date.today()) + "_" \
                           + "\nToday's winning number is... **" \
                           + str(win_number) + "**\n\n__The lucky **basic** winners:__  " \
                           + std_winners_string + "\n__The lucky **premium** winners:__  " \
                           + prem_winners_string
    global_announcement3 = "__**PATCH ANNOUNCEMENT**__\nPatch **2.7** is here! Use **=adopt** command for your own pet!"

    # embed shop announcement and lottery announcement, and set thumbnails of a shopping cart and "money rain frog" gif
    em = discord.Embed(description=global_announcement1, colour=0x607d4a)
    em.set_thumbnail(url="https://i.imgur.com/rS6tXmD.gif")
    em2 = discord.Embed(description=global_announcement2, colour=0x607d4a)
    em2.set_thumbnail(url="https://cdn.discordapp.com/emojis/525200274340577290.gif?size=64")
    em3 = discord.Embed(description=global_announcement3, colour=0x607d4a)
    em3.set_thumbnail(url="http://i66.tinypic.com/25g7akg.jpg")


    # for each server the bot is in, post the lottery results in the lottery channel
    for server in client.servers:
        # try to get the server's announcement status
        # if they turned off announcements, skip to next loop iteration
        try:
            if db.get_server_announcements_status(server.id) == 0:
                continue
        except:
            pass
        # create boolean for each server, to dictate whether or not the 'lottery' channel could be located
        channel_found = 0
        for channel in server.channels:
            try:
                if channel.name == 'lottery':
                    channel_found = 1
                    await client.send_message(channel, embed=em)
                    await client.send_message(channel, embed=em2)
                    await client.send_message(channel, embed=em3)
            except:
                pass

        # if there were no channels found with the name 'lottery'.....
        # make the channel, then send the results
        if channel_found == 0:
            try:
                channel = await client.create_channel(server, 'lottery', type=discord.ChannelType.text)
                await client.send_message(channel, embed=em)
                await client.send_message(channel, embed=em2)
            except:
                # if the bot failed to make the channel, simply move on
                pass


    """ PERFORM DAILY TOURNAMENT MAINTENANCE NOW! """
    for server in client.servers:
        server_fighters_ids = db.get_server_tourney_members(server.id)
        # only do anything else if the server has more than 1 entry
        # need more than 1 fighter entry to have a tournament
        if len(server_fighters_ids) > 1:
            total_stats_pool = 0
            server_fighters_weights = []
            # 2 loops necessary here for the math:
            # we need the sum pool of stats of all fighters in the server
            for fighter_id in server_fighters_ids:
                fighter = Users(fighter_id)
                # algorithm for calculating a fighter's stats in tourneys: (item score + user level*2 + 22)
                fighter_stats = (fighter.get_user_item_score() + (fighter.get_user_level(0) * 2)) + 22
                total_stats_pool += fighter_stats

            # now we need to divide each fighter's stats by the sum stat pool in order to get specific win chances
            for fighter_id in server_fighters_ids:
                fighter = Users(fighter_id)
                # algorithm for calculating a fighter's stats in tourneys: (item score + user level*2 + 22)
                fighter_stats = (fighter.get_user_item_score() + (fighter.get_user_level(0) * 2)) + 22
                fighter_weight = fighter_stats / total_stats_pool
                server_fighters_weights.append(fighter_weight)

            # print("\nPool: " + str(total_stats_pool) + " All fighters: " + str(
            #     server_fighters_ids) + " All weights: " + str(server_fighters_weights))

            # https://docs.scipy.org/doc/numpy/reference/generated/numpy.random.choice.html
            # random's choices package did not offer a "weighted shuffle"
            # decided to use numpy here for the weighted choice, because it can do a a "weighted shuffle"
            # a weighted shuffle was required to randomly generate an ordered list of winners influenced by weights
            server_winners = numpy.random.choice(server_fighters_ids, size=len(server_fighters_ids),
                                                 replace=False, p=server_fighters_weights)

            # make object of first and second place users
            first_place = Users(server_winners[0])
            second_place = Users(server_winners[1])

            # update their money accordingly
            prize1 = first_place.get_user_level(0) * 170
            prize2 = second_place.get_user_level(0) * 100
            first_place.update_user_money(prize1)
            second_place.update_user_money(prize2)
            # first place will count as a win in records
            first_place.update_user_records(0, 1, prize1)
            # second place will count as a win in records
            second_place.update_user_records(0, 1, prize2)

            # prepare string for local server tourney announcement
            # have to insert encode \u200B for spaces when using discord encoding
            local_server_announcement = '__**TOURNEY ANNOUNCEMENT**__ \u200B \u200B_' + str(date.today())\
                                        + '_\n\n**:trophy: 1st place: ** ' + '<@' \
                                        + server_winners[0] + '> :trophy:  __Prize__: **$' + str(prize1) \
                                        + '**\n' + '**:trophy: 2nd place:** ' + '<@' + server_winners[1] \
                                        + '> :trophy:  __Prize__: **$' + str(prize2) + '**\n'

            # find the channel in the server and state the results
            for channel in server.channels:
                # try to get the server's announcement status
                # if they turned off announcements, skip to next loop iteration
                try:
                    if db.get_server_announcements_status(server.id) == 0:
                        continue
                except:
                    pass
                if channel.name == 'lottery':
                    # if there were more than 2 fighters, make an "honorable mentions" string to append to announcement
                    if len(server_fighters_ids) > 2:
                        # counter to represent placings- losers list will start at 3rd place
                        counter = 3
                        loser_string = '\n__Honorable mentions__\n'
                        for loser in server_winners[2:]:
                            user = Users(server_winners[counter-1])
                            user.update_user_records(1, 0, 0)
                            if counter == 3:
                                loser_string += ('**' + str(counter) + 'rd place: <@' + loser + '>**\n')
                            else:
                                loser_string += ('**' + str(counter) + 'th place: <@' + loser + '>**\n')
                            counter += 1
                        local_server_announcement += loser_string

                        # embed combined announcement, with emoji of 64x64 "nunchuck frog", then send it
                        em = discord.Embed(description=local_server_announcement, colour=0x607d4a)
                        em.set_thumbnail(url="https://cdn.discordapp.com/emojis/493220414206509056.gif?size=64")
                        try:
                            await client.send_message(channel, embed=em)
                        except:
                            pass

                    # else if only 2 entries in the server's tournament, just send first and second place results
                    elif len(server_fighters_ids) == 2:
                        # embed announcement, with emoji of 64x64 "nunchuck frog", then send it
                        em = discord.Embed(description=local_server_announcement, colour=0x607d4a)
                        em.set_thumbnail(url="https://cdn.discordapp.com/emojis/493220414206509056.gif?size=64")
                        try:
                            await client.send_message(channel, embed=em)
                        except:
                            pass

    # reset tournament entries after every server's tournament is processed
    db.reset_tourney()

    # end this daily maintenance program
    sys.exit(0)

client.run(TOKEN)
