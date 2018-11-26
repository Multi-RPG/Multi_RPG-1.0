#!/usr/bin/env python3
import discord
import random
import datetime
import configparser
import sys
from discord.ext import commands
from pathlib import Path

# set up parser to config through our .ini file with our bot's token
config = configparser.ConfigParser()
bot_token_path = Path("tokens/tokenbot.ini") # use forward slash "/" for path directories
# confirm the token is located in the above path
if bot_token_path.is_file():
    config.read(bot_token_path)
    # we now have the bot's token
    TOKEN = config.get('BOT1', 'token')
else:
    print("\n","User tokens not found at: ",bot_token_path,"... Please correct file path in Main.py file.")
    sys.exit()

    
client = commands.Bot(command_prefix=["=", "%"])
client.remove_command('help')

@client.event
async def on_ready():
    print('Logged in as\n'
          + client.user.name + '\n'
          + client.user.id + '\n'
          + '---------')
    await client.change_presence(game=discord.Game(name='=help for commands'))

@client.event
async def on_message(message):
    # when we don't want the bot to reply to itself
    if message.author == client.user:
        return

    # need this statement for bot to recognize commands
    await client.process_commands(message)

@client.command(name='help', description='command information', brief='show this message', aliases=['h'], pass_context = True)
async def helper(context):
    # using discord's "ml" language coloring scheme for the encoded help message
    msg = '```ml\n' \
          'Utilities:\n' \
          '  =clear          use "=clear" or "=clear X", -- X being #  messages \n' \
          '  =code           use "=code" to view this bot\'s source code\n' \
          '  =invite         use "=invite" to view the bot\'s invitation link\n' \
          '  =id             use "=id" to view your personal discord ID\n' \
          'Account:\n' \
          '  =create         use "=create" to make a account\n' \
          '  =delete         use "=delete" to delete your account\n' \
          '  =levelup        use "=levelup" to level up your account\n' \
          '                  (this gives 2% increased battle win probability)\n\n' \
          '  =level          use "=level" or "=level @user" to print account level\n' \
          '  =stats          use "=stats" or "=stats @user" to print battle stats\n' \
          '  =money          use "=money" or "=money @user" to print bank balance\n' \
          '  =give           use "=give @user X" -- X being money to give a user\n' \
          'Games For Money:\n' \
          '  =rob            use "=rob" for a 6/10 chance to mug a fellow player\n' \
          '  =fight          use "=fight @user X" -- X being money to bet\n' \
          '  =flip           use "=flip" or "=flip X" or "=flip X Y" \n' \
          '                  -- X being heads or tails guess\n' \
          '                  -- Y being amount to bet\n\n' \
          '  =hangman        use "=hangman" or "=hangman X", -- X being a category # \n' \
          '                  use "=hm cats" for category numbers\n' \
          '                  use "stop" or "cancel" to stop game\n' \
          'Meme Maker:  \n' \
          '  =custom         =custom to create a custom Twitter-style meme \n' \
          '  =pigeon         =pigeon "boy" "butterfly" "is this a pidgeon?" \n' \
          '  =boyfriend      =boyfriend "new girl" "distracted boyfriend" "girlfriend"\n' \
          '  =brain          =brain "stage1" "stage2" "stage3" "stage4"\n' \
          '  =twobuttons     =twobuttons "option 1" "option2"\n' \
          '  =slapbutton     =slapbutton "cause" "reaction"\n' \
          '  =leftexit       =leftexit "left" "right" "car"\n' \
          '  =trumporder     =trumporder "order"\n' \
          '  =reasonstolive  =reasonstolive "reasons"\n' \
          '  =bookfacts      =bookfacts "facts"```'
    await client.send_message(context.message.author, msg)

# Commands error handling
@client.event
async def on_command_error(error, context):
    if isinstance(error, commands.CommandOnCooldown):
        # error.retry_after returns float, need to cast to integer without decimals
        # now convert to proper HH:MM:SS format and print the cooldown
        time = str(datetime.timedelta(seconds=int(error.retry_after)))
        await client.send_message(context.message.channel, content=' You are on cooldown: ' + time)

    if isinstance(error, commands.CommandNotFound):
        return

if __name__ == "__main__":
    for extension in ["Games", "Utilities", "Memes", "Account"]:
        try:
            client.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

        
client.run(TOKEN)