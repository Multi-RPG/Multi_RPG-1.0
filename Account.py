#!/usr/bin/env python3
import re
import asyncio
import discord
from discord.ext import commands
from DiscordBotsOrgApi import DiscordBotsOrgAPI
from Users import Users

# short decorator function declaration, confirm that command user has an account in database
def has_account():
    def predicate(ctx):
        user = Users(ctx.message.author.id)
        if user.find_user() == 0:
            return False
        else:
            return True

    return commands.check(predicate)

# short decorator function declaration, confirm that command user has voted for the bot on discordbots.org
def has_voted():
    def predicate(ctx):
        # create object of discordbotsapi to make use of the api
        checker = DiscordBotsOrgAPI()
        # check if the user attempting to use this command has voted for the bot within 24 hours
        # if they have not voted recently, let the error handler in Main.py give the proper error message
        if checker.check_upvote(ctx.message.author.id) == 0:
            return False
        else:
            return True

    return commands.check(predicate)

class Account:
    def __init__(self, client):
        self.client = client

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='create', description='make a user',
                      brief='start a user account', aliases=['register'], pass_context=True)
    async def register(self, context):
        # create new user instance with their discord ID to store in database
        new_user = Users(context.message.author.id)

        if new_user.find_user() == 1:
            await self.client.say('<:worrymag1:531214786646507540> You **already** have an account registered!')
            return

        em = discord.Embed(title="", colour=0x607d4a)
        em.add_field(name=context.message.author.display_name, value=new_user.add_user(), inline=True)
        em.set_thumbnail(url=context.message.author.avatar_url)
        await self.client.say(embed=em)


    @has_account()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='money', aliases=['m', 'MONEY'], pass_context=True)
    async def money(self, context, *args):
        # this 'try' will process if they want to check another person's bank account
        # it will only process if they passed that user as an argument
        try:
            # use regex to extract only numbers to get their discord ID,
            # ex: <@348195501025394688> to 348195501025394688
            # create user instance with their target's discord ID, check database for their money field
            target_id = re.findall("\d+", args[0])[0]
            target = Users(target_id)
            if target.find_user() == 0:
                await self.client.say('Target does not have account.')
                return

            # get_member() returns the "member" object that matches an id provided
            discord_member_target = context.message.server.get_member(target_id)

            # embed the money retrieved from get_user_money(), set thumbnail to 64x64 version of target's id
            em = discord.Embed(title="", colour=0x607d4a)
            em.add_field(name=discord_member_target.display_name, value="**:moneybag: ** " + target.get_user_money(), inline=True)
            thumb_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.webp?size=64".format(discord_member_target)
            em.set_thumbnail(url=thumb_url)

            await self.client.send_message(context.message.channel, context.message.author.mention, embed=em)
        # if they passed no parameter, get their own money
        except:
            # create user instance with their discord ID, check database for their money field
            user = Users(context.message.author.id)

            # embed the money retrieved from get_user_money(), set thumbnail to 64x64 version of user's id
            em = discord.Embed(title="", colour=0x607d4a)
            em.add_field(name=context.message.author.display_name, value="**:moneybag: ** " + user.get_user_money(), inline=True)
            thumb_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.webp?size=64".format(context.message.author)
            em.set_thumbnail(url=thumb_url)

            await self.client.send_message(context.message.channel, context.message.author.mention, embed=em)

        # delete original message to reduce spam
        await self.client.delete_message(context.message)

    @has_account()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='level', aliases=['LEVEL', 'lvl', 'LVL'], pass_context=True)
    async def level(self, context, *args):
        # this 'try' will process if they want to check another player's level
        # it will only process if they passed that user as an argument
        try:
            # use regex to extract only numbers to get their discord ID,
            # ex: <@348195501025394688> to 348195501025394688
            # create user instance with their target's discord ID, check database for their level field
            target_id = re.findall("\d+", args[0])[0]
            target = Users(target_id)
            if target.find_user() == 0:
                await self.client.say('Target does not have account.')
                return

            # get_member() returns the "member" object that matches an id provided
            discord_member_target = context.message.server.get_member(target_id)

            # embed the level retrieved from get_user_level(), set thumbnail to 64x64 version of target's id
            em = discord.Embed(title="", colour=0x607d4a)
            em.add_field(name=discord_member_target.display_name, value="**Level** " + target.get_user_level(), inline=True)
            thumb_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.webp?size=64".format(discord_member_target)
            em.set_thumbnail(url=thumb_url)

            await self.client.send_message(context.message.channel, context.message.author.mention, embed=em)
        # if they passed no parameter, get their own level
        except:
            # create user instance with their discord ID, check database for their level field
            user = Users(context.message.author.id)

            # embed the level retrieved from get_user_level(), set thumbnail to 64x64 version of user's id
            em = discord.Embed(title="", colour=0x607d4a)
            em.add_field(name=context.message.author.display_name, value="**Level** " + user.get_user_level(), inline=True)
            thumb_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.webp?size=64".format(context.message.author)
            em.set_thumbnail(url=thumb_url)

            await self.client.send_message(context.message.channel, context.message.author.mention, embed=em)

        # delete original message to reduce spam
        await self.client.delete_message(context.message)

    @has_account()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='give', aliases=['DONATE', 'GIVE', 'pay', 'donate', 'PAY', 'gift', 'GIFT'], pass_context=True)
    async def give(self, context, *args):
        # will automatically go to exception if all arguments weren't supplied correctly
        try:
            receiver_string = args[0]
            amnt = int(args[1])
            if amnt < 1:
                await self.client.say("Can’t GIFT DEBT!")
                return
            # create user instance with their discord ID, check database for their level field
            donator = Users(context.message.author.id)
            # use regex to extract only numbers from "receiver_string" to get their discord ID,
            # ex: <@348195501025394688> to 348195501025394688
            receiver = Users(re.findall("\d+", receiver_string)[0])

            # check if receiver has account
            if receiver.find_user() == 0:
                await self.client.say(context.message.author.mention +
                                      " The target doesn't have an account."
                                      "\nUse **=create** to make one.")
                return
            # check if donator has enough money for the donation
            # pass 0 to return integer version of money, see USERS.PY function
            if int(amnt) > donator.get_user_money(0):
                await self.client.say(context.message.author.mention +
                                      " You don't have enough money for that donation..."
                                      " <a:pepehands:485869482602922021> ")
                return

            # pass the donation amount, pass the receiver user object, and pass the receiver's string name
            msg = context.message.author.mention + ' ' + donator.donate_money(int(amnt), receiver, receiver_string)
            # embed the donation message, put a heartwarming emoji size 64x64 as the thumbnail
            em = discord.Embed(title="", colour=0x607d4a)
            em.add_field(name="DONATION ALERT", value=msg, inline=True)
            em.set_thumbnail(url="https://cdn.discordapp.com/emojis/526815183553822721.webp?size=64")
            await self.client.say(embed=em)
            await self.client.delete_message(context.message)
        except:
            await self.client.say(context.message.author.mention +
                                  '```ml\nuse =give like so: **=give @user X**    -- X being amnt of money to give```')

    @has_account()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='stats',
                      aliases=['battles', 'BRECORDS', 'STATS', 'profile', 'PROFILE', 'gear', 'GEAR'], pass_context=True)
    async def profile_stats(self, context, *args):
        # this 'try' will process if they want to check another person's battle records
        # it will only process if they passed that user as an argument
        try:
            # use regex to extract only numbers to get their discord ID,
            # ex: <@348195501025394688> to 348195501025394688
            # create user instance with their target's discord ID, check database for their money field
            target_id = re.findall("\d+", args[0])[0]
            target = Users(target_id)
            if target.find_user() == 0:
                await self.client.say('Target does not have account.')
                return

            # get_member() returns the "member" object that matches an id provided
            discord_member_target = context.message.server.get_member(target_id)
            target_avatar_url = discord_member_target.avatar_url

            # embed the statistics retrieved from get_user_stats(), set thumbnail to target's id
            em = discord.Embed(title="", colour=0x607d4a)
            em.add_field(name=discord_member_target.display_name, value=target.get_user_stats(), inline=True)
            em.set_thumbnail(url=target_avatar_url)

            await self.client.send_message(context.message.channel, context.message.author.mention, embed=em)


        # if they passed no parameter, or user was not found, get their own records
        except:
            # create user instance with their discord ID, check database for their level field
            user = Users(context.message.author.id)

            # embed the statistics retrieved from get_user_stats(), set thumbnail to user's id
            em = discord.Embed(title="", colour=0x607d4a)
            em.add_field(name=context.message.author.display_name, value=user.get_user_stats(), inline=True)
            em.set_thumbnail(url=context.message.author.avatar_url)

            await self.client.send_message(context.message.channel, context.message.author.mention, embed=em)

    @has_account()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='levelup', aliases=['lup', 'LEVELUP'], pass_context=True)
    async def levelup(self, context):
        # create instance of user who wants to level-up
        user = Users(context.message.author.id)
        # get the user's current level
        # calculate the cost of their next level-up
        user_level = user.get_user_level(0) # get int version of level, SEE USERS.PY
        # level up cost algorithm, inspired by D&D algorithm
        level_up_cost = int(300 * ((user_level + 1) ** 1.72) - (300 * user_level))

        if user_level == 1:
            level_up_cost = 399
        elif user_level > 7:
            level_up_cost = int(300 * ((user_level + 1) ** 1.8) - (300 * user_level))
        elif user_level > 9:
            level_up_cost = int(300 * ((user_level + 1) ** 1.91) - (300 * user_level))
        elif user_level == 15:
            await self.client.say('You are already level 15, the max level!')
            return

        # check if they have enough money for a level-up
        if user.get_user_money(0) < level_up_cost:
            error_msg = await self.client.say(context.message.author.mention + ' Not enough money for level-up...'
                                                                             + ' <a:pepehands:485869482602922021>\n'
                                                                             + '** **\nAccount balance: '
                                                                             + user.get_user_money() + '\nLevel **'
                                                                             + str(user_level + 1) + '** requires: **$'
                                                                             + str(level_up_cost) + '**')
            # wait 15 seconds then delete error message and original message to reduce spam
            await asyncio.sleep(15)
            await self.client.delete_message(error_msg)
            await self.client.delete_message(context.message)
            return

        # passed conditional, so they have enough money to level up
        # confirm if they really want to level-up
        msg = '\nAccount balance: ' + user.get_user_money() \
              + '\nLevel **' + str(user_level + 1) \
              + '** requires: **$' + str(level_up_cost) \
              + '**\n** **\nDo you want to level-up?' \
              + ' Type **confirm** to confirm.'

        # embed the confirmation prompt, set thumbnail to user's id of max size
        em = discord.Embed(description=msg, colour=0x607d4a)
        thumb_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.webp?size=1024".format(context.message.author)
        em.set_thumbnail(url=thumb_url)

        await self.client.send_message(context.message.channel, context.message.author.mention, embed=em)


        # wait for user's input
        confirm = await self.client.wait_for_message(author=context.message.author, timeout=60)
        if confirm.clean_content.upper() == 'CONFIRM':
            # check if they tried to exploit the code by spending all their money before confirming
            if user.get_user_money(0) < level_up_cost:
                await self.client.say(context.message.author.mention + " You spent money before confirming...")
                return
            # deduct the level-up cost from their account
            user.update_user_money(level_up_cost*-1)
            # embed the confirmation message, set thumbnail to user's id of size 64x64
            # increase level by 1 and print new level
            em = discord.Embed(title="", colour=0x607d4a)
            em.add_field(name=context.message.author.display_name, value=user.update_user_level(), inline=True)
            thumb_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.webp?size=64".format(
                context.message.author)
            em.set_thumbnail(url=thumb_url)
            await self.client.say(embed=em)
        else:
            await self.client.say(context.message.author.mention + ' Cancelled level-up.')


    @has_account()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    @commands.command(name='daily', aliases=['DAILY', 'dailygamble'], pass_context=True)
    async def daily(self, context):
        # create instance of user who wants to get their daily money
        user = Users(context.message.author.id)
        # get the user's current level
        # calculate the cost of their next level-up
        user_level = user.get_user_level(0) # get int version of level, SEE USERS.PY
        dailyreward = user_level * 60

        msg = '<a:worryswipe:525755450218643496> Daily **$' + str(dailyreward) \
              + '** received! <a:worryswipe:525755450218643496>\n' + user.update_user_money(dailyreward)

        # embed the confirmation message, set thumbnail to user's id
        em = discord.Embed(title="", colour=0x607d4a)
        em.add_field(name=context.message.author.display_name, value=msg, inline=True)
        em.set_thumbnail(url=context.message.author.avatar_url)
        await self.client.say(embed=em)

    @has_voted()
    @has_account()
    @commands.cooldown(1, 43200, commands.BucketType.user)
    @commands.command(name='daily2', aliases=['DAILY2', 'bonus', 'votebonus'], pass_context=True)
    async def daily2(self, context):
        # create instance of user who earned their vote bonus
        user = Users(context.message.author.id)
        # get the user's current level
        user_level = user.get_user_level(0) # get int version of level, SEE USERS.PY
        dailyreward = user_level * 50

        msg = '<a:worryswipe:525755450218643496> Daily **$' + str(dailyreward) \
              + '** received! <a:worryswipe:525755450218643496>\n' + user.update_user_money(dailyreward)

        # embed the confirmation message, set thumbnail to user's id
        em = discord.Embed(title="", colour=0x607d4a)
        em.add_field(name="Thanks for voting, {}!".format(context.message.author.display_name), value=msg, inline=True)
        em.set_thumbnail(url=context.message.author.avatar_url)
        await self.client.say(embed=em)

    @has_account()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='toggle', aliases=['togglepeace', 'TOGGLEPEACE', 'peace', 'PEACE',], pass_context=True)
    async def toggle_peace(self, context):
        # create instance of user who wants to get their daily money
        user = Users(context.message.author.id)
        user_peace_status = user.get_user_peace_status()
        user_peace_cooldown = user.get_user_peace_cooldown()
        if user_peace_status == 0 and user_peace_cooldown == 0:
            msg = ':dove: Would you like to enable peace status? :dove:\n\nType **confirm** to enter peace mode\n' \
                  'Type **cancel** to cancel\n\n' \
                  '_Note: \u200B \u200B \u200B This makes you exempt from users who use =rob @user' \
                  '\nNote2: \u200B In exchange, you will not be able to =rob @user' \
                  '\nNote3: You can still use =rob or be robbed randomly from =rob_'
            # embed the confirmation message, set thumbnail to user's id
            em = discord.Embed(title="", colour=0x607d4a)
            em.add_field(name=context.message.author.display_name, value=msg,
                         inline=True)
            em.set_thumbnail(url=context.message.author.avatar_url)
            await self.client.say(embed=em)

            # wait for a "confirm" response from the user to process the peace toggle
            # if it is not "confirm", cancel toggle
            response = await self.client.wait_for_message(author=context.message.author, timeout=20)
            if response.clean_content.upper() == 'CONFIRM':
                user.toggle_user_peace_status()
                user.update_user_peace_cooldown()
                confirmation = ":dove: You are now **in peace** status :dove:" \
                               "\n\nYou are **unable** to turn it off until Monday at 7 AM PST!"

                # embed the confirmation string, add the user's avatar to it, and send it
                em = discord.Embed(title="", colour=0x607d4a)
                em.add_field(name=context.message.author.display_name, value=confirmation, inline=True)
                em.set_thumbnail(url=context.message.author.avatar_url)
                await self.client.say(embed=em)
                return
            else:
                await self.client.say(context.message.author.mention + ' Cancelled peace toggle-on!')
                return

        elif user_peace_status == 1 and user_peace_cooldown == 0:
            msg = ':dove: You are currently **in peace** status and **able** to turn it off :dove:'  \
                  '\n\nType **confirm** to turn off peace mode\nType **cancel** to cancel\n\n' \
                  '_Note: This will enable users to use =rob @user on you_'
            # embed the confirmation message, set thumbnail to user's id
            em = discord.Embed(description=msg, colour=0x607d4a)
            em.set_thumbnail(url=context.message.author.avatar_url)
            await self.client.say(embed=em)

            # wait for a "confirm" response from the user to process the peace toggle
            # if it is not "confirm", cancel toggle
            response = await self.client.wait_for_message(author=context.message.author, timeout=20)
            if response.clean_content.upper() == 'CONFIRM':
                user.toggle_user_peace_status()
                confirmation = ":dove: You are now **out of peace** status :dove:\n\n_Note: =rob @user is now available_"

                # embed the confirmation string, add the user's avatar to it, and send it
                em = discord.Embed(title="", colour=0x607d4a)
                em.add_field(name=context.message.author.display_name, value=confirmation, inline=True)
                em.set_thumbnail(url=context.message.author.avatar_url)
                await self.client.say(embed=em)
                return
            else:
                await self.client.say(context.message.author.mention + ' Cancelled peace toggle-off!')
                return

        elif user_peace_cooldown == 1:
            msg = ':dove: You are currently **in peace** status :dove:' \
                  '\nYou are **unable** to turn it off until Monday at 7 AM PST!'
            # embed the confirmation message, set thumbnail to user's id
            em = discord.Embed(description=msg, colour=0x607d4a)
            em.set_thumbnail(url="https://cdn.discordapp.com/emojis/440598341877891083.png?size=40")
            await self.client.say(embed=em)
            return


def setup(client):
    client.add_cog(Account(client))
