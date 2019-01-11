#!/usr/bin/env python3
import configparser
import sys
import random
import discord
import numpy
from numpy import random
from Users import Users
from Database import Database
from discord.ext import commands
from pathlib import Path
from datetime import date

# IMPORTANT: FOR FULL AUTOMATION, SCHEDULE THIS FILE TO RUN AUTOMATICALLY AT AN INTERVAL.
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

    # open database
    db = Database(0)
    db.connect()

    ''' PERFORM DAILY SHOP MAINTENANCE NOW! '''
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
    # each item has a 14% chance to be inserted into the daily shop
    for item in config.sections():
        if 14 >= random.randint(1, 100) >= 1:
            item_name = config.get(item, 'name')
            item_type = config.get(item, 'type')
            item_level = config.get(item, 'level')
            item_price = config.get(item, 'price')

            db.insert_shop_item(item_name, item_type, item_level, item_price)


    ''' PERFORM DAILY LOTTERY MAINTENANCE NOW'''
    # generate a random winning number 1-5
    win_number = 1
    # get python list of winner ticket id's who match today's winning number
    std_winners, prem_winners = db.get_lottery_winners(win_number)
    # we have today's winners now, so reset lottery
    db.reset_lottery()
    std_winners_string = ''
    for winner in std_winners:
        # create instance of each basic ticket user who won, and update their money
        user = Users(winner)
        user.update_user_money(user.get_user_level(0) * 80)
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

    global_announcement = "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁\n" \
                          + ":shopping_cart: __**SHOP ANNOUNCEMENT**__ " + ":shopping_cart:" \
                          + "_" + str(date.today()) + "_" \
                          + "\nDaily shop has been reset! Check out **=shop**!\n" \
                          + "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁\n" \
                          + "<a:worrycash:525200274340577290> __**LOTTERY ANNOUNCEMENT**__" \
                          + " <a:worrycash:525200274340577290> _" + str(date.today()) + "_" \
                          + "\nToday's winning number is... **" \
                          + str(win_number) + "**\n\n__The lucky **basic** winners:__  " \
                          + std_winners_string + "\n__The lucky **premium** winners:__  " \
                          + prem_winners_string

    # for each server the bot is in, post the lottery results in the lottery channel
    for server in client.servers:
        # create boolean for each server, to dictate whether or not the 'lottery' channel could be located
        channel_found = 0
        for channel in server.channels:
            try:
                if channel.name == 'lottery':
                    channel_found = 1
                    await client.send_message(channel, global_announcement)
            except:
                pass

        # if there were no channels found with the name 'lottery'.....
        # make the channel, then send the results
        if channel_found == 0:
            try:
                channel = await client.create_channel(server, 'lottery', type=discord.ChannelType.text)
                await client.send_message(channel, global_announcement)
            except:
                # if the bot failed to make the channel, simply move on
                pass


    ''' PERFORM DAILY TOURNAMENT MAINTENANCE NOW! '''
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
            local_server_announcement = '▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁\n' \
                                        ':crossed_swords: __**TOURNEY ANNOUNCEMENT**__ :crossed_swords: _' \
                                        + str(date.today()) + '_\n\n**:trophy: 1st place: ** ' + '<@' \
                                        + server_winners[0] + '> :trophy:  __Prize__: **$' + str(prize1) \
                                        + '**\n' + \
                                        '**:trophy: 2nd place:** ' + '<@' + server_winners[1] \
                                        + '> :trophy:  __Prize__: **$' + str(prize2) + '**\n'

            # find the channel in the server and state the results
            for channel in server.channels:
                if channel.name == 'lottery':
                    await client.send_message(channel, local_server_announcement)
                    counter = 3
                    # if there were more than 2 fighters, list the honorable mentions
                    if len(server_fighters_ids) > 2:
                        loser_string = '\n__Honorable mentions__\n'
                        for loser in server_winners[2:]:
                            user = Users(server_winners[counter-1])
                            user.update_user_records(1, 0, 0)
                            if counter == 3:
                                loser_string += ('**' + str(counter) +'rd place: <@' + loser + '>**\n')
                            else:
                                loser_string += ('**' + str(counter) +'th place: <@' + loser + '>**\n')
                            counter += 1

                        await client.send_message(channel, loser_string)


    # reset tournament entries after every server's tournament is processed
    db.reset_tourney()

    # end this daily maintenance program
    sys.exit(0)

client.run(TOKEN)
