#!/usr/bin/env python3
import discord
import configparser
import sys
import datetime
import logging
from discord.ext import commands
from pathlib import Path

# set our bot's prefix and remove the default help command
client = commands.Bot(command_prefix=["=", "%"])
client.remove_command('help')

# set up logging for command errors
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler = logging.FileHandler('logs/commands_errors.txt')
handler.setFormatter(formatter)

commands_logger = logging.getLogger('commands_logger')
commands_logger.setLevel(logging.INFO)
commands_logger.addHandler(handler)


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

@client.command(name='help', description='command information', brief='commands', aliases=['h'], pass_context=True)
async def helper(context):
    # using discord's "ml" language coloring scheme for the encoded help message
    msg = '```ml\n' \
          'Utilities:\n' \
          '  =clear          use "=clear" or "=clear X", -- X being #  messages \n' \
          '  =code           use "=code" to view this bot\'s source code\n' \
          '  =invite         use "=invite" to view the bot\'s invitation link\n' \
          '  =id             use "=id" to view your personal discord ID\n' \
          '  =remindme       use "=remindme "message" X"  -- X being the timer\n' \
          'Account:\n' \
          '  =create         use "=create" to make a account\n' \
          '  =daily          use "=daily" for free money equal to 60x your level\n' \
          '  =daily2         use "=daily2" for free money equal to 50x your level\n' \
          '  =shop           use "=shop" to view the daily shop items\n' \
          '  =buy            use "=buy X" to purchase shop item  -- X being item #\n' \
          '  =levelup        use "=levelup" to level up your account\n' \
          '                  (this results in higher profits & battle successes)\n\n' \
          '  =profile        use "=profile" or "=profile @user" to print battle & gear stats\n' \
          '  =level          use "=level" or "=level @user" to print account level\n' \
          '  =money          use "=money" or "=money @user" to print bank balance\n' \
          '  =give           use "=give @user X" -- X being money to give a user\n```'
    msg2 = '```ml\n' \
          'Games For Money:\n' \
          '  =lotto          use "=lotto" for a 1/5 chance to win 100x your level each day\n' \
          '  =lotto2         use "=lotto2" for a 1/5 chance to win 170x your level each day\n' \
          '  =tourney        use "=tourney" to compete in a server-based, daily FFA tournament\n' \
          '                  NOTE: this event takes item level & user level into calculation\n' \
          '                  NOTE: this event requires AT LEAST 2 entries from your server\n' \
          '                  NOTE: the reward is 170x your level for first, 100x for second\n' \
          '  =rob            use "=rob" for a 7/10 chance to mug a random player\n' \
          '  =rob            use "=rob @user" for a 6.5/10 chance to mug a specified player\n' \
          '  =fight          use "=fight @user X" -- X being money to bet\n' \
          '  =flip           use "=flip" or "=flip X" or "=flip X Y" \n' \
          '                  -- X being heads or tails guess\n' \
          '                  -- Y being amount to bet\n\n' \
          '  =hangman        use "=hangman" or "=hangman X", -- X being a category # \n' \
          '                  use "=hm cats" for category numbers\n' \
          '                  use "stop" or "cancel" to stop game\n' \
          '                  NOTE: the reward is 8x your level\n' \
          'Meme Maker:  \n' \
          '  =custom         =custom to create a custom Twitter-style meme \n' \
          '  =changemymind   =changemymind "opinion" \n' \
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
    await client.send_message(context.message.author, msg2)


# Commands error handling
@client.event
async def on_command_error(error, context):
    if isinstance(error, commands.CommandOnCooldown):
        # error.retry_after returns float, need to cast to integer without decimals
        # now convert to proper HH:MM:SS format and print the cooldown
        time = str(datetime.timedelta(seconds=int(error.retry_after)))
        await client.send_message(context.message.channel, content=' You are on cooldown: ' + time)

    elif isinstance(error, commands.CommandNotFound):
        commands_logger.info(str(error) +
                             "\nInitiated by: {}, ID: {}".format(context.message.author.name, context.message.author.id))

    # we use command checks when checking if user has account in our database or not
    elif isinstance(error, commands.CheckFailure):
        if "daily2" in str(error):
            error_msg = "Failed! You have not voted within the last 24 hours." \
                        "\nhttps://discordbots.org/bot/486349031224639488/vote"
            em = discord.Embed(title=context.message.author.display_name, description=error_msg, colour=0x607d4a)
            em.set_thumbnail(url="https://cdn.discordapp.com/emojis/440598341877891083.png?size=64")
            return await client.send_message(context.message.channel, embed=em)
        else:
            return await client.send_message(context.message.channel, " No account found.\nUse **=create** to make one.")
    else:
        commands_logger.info(str(error) + " in command: " + str(context.command) +
                             "\nUser tried: " + str(context.message.clean_content) +
                             "\nInitiated by: {}, ID: {}".format(context.message.author.name, context.message.author.id))

if __name__ == "__main__":
    for extension in ["Games", "Utilities", "Memes", "Account", "Lottery", "Shop", "DiscordBotsOrgApi"]:
        try:
            client.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))


# set up parser to config through our .ini file with our bot's token
config = configparser.ConfigParser()
bot_token_path = Path("tokens/tokenbot.ini") # use forward slash "/" for path directories
# confirm the token is located in the above path
if bot_token_path.is_file():
    config.read(bot_token_path)
    # we now have the bot's token
    TOKEN = config.get('BOT1', 'token')
else:
    print("\n","Discord bot token not found at: ",bot_token_path,"... Please correct file path in Main.py file.")
    sys.exit()

client.run(TOKEN)