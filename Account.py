#!/usr/bin/env python3
import re
from discord.ext import commands
from Users import Users

class Account:
    def __init__(self, client):
        self.client = client

    @commands.command(name='create', description='make a user',
                      brief='start a user account', aliases=['register'], pass_context=True)
    async def register(self, context):
        # create new user instance with their discord ID to store in database
        new_user = Users(context.message.author.id)
        msg = new_user.add_user()
        await self.client.say(context.message.author.mention + msg)

    @commands.command(name='delete', description='delete your user',
                      brief='delete your user account', aliases=['del'], pass_context=True)
    async def delete(self, context):
        # create user instance with their discord ID, delete user from database based off their discord ID
        await self.client.say('Do you really want to delete your account? Type **"confirm"** to confirm.')
        guess = await self.client.wait_for_message(author=context.message.author, timeout=60) # wait for user's input
        if guess.clean_content.upper() == 'CONFIRM':
            user = Users(context.message.author.id)
            await self.client.say(context.message.author.mention + user.delete_user())
        else:
            await self.client.say(context.message.author.mention + ' Cancelled deletion of account')

    @commands.command(name='money', aliases=['m'], pass_context=True)
    async def money(self, context, *args):
        # this 'try' will process if they want to check another person's bank account
        # it will only process if they passed that user as an argument
        try:
            # use regex to extract only numbers to get their discord ID,
            # ex: <@348195501025394688> to 348195501025394688
            # create user instance with their discord ID, check database for their money field
            user = Users(re.findall("\d+", args[0])[0])
            await self.client.say(context.message.author.mention +
                                  " That user's account balance: " + user.get_user_money())
        # if they passed no parameters, get their own money
        except:
            # create user instance with their discord ID, check database for their money field
            user = Users(context.message.author.id)
            await self.client.say(context.message.author.mention +
                                  " Your account balance: " + user.get_user_money())

    @commands.command(name='level', aliases=['LEVEL', 'lvl', 'LVL'], pass_context=True)
    async def level(self, context):
        # create user instance with their discord ID, check database for their level field
        user = Users(context.message.author.id)
        await self.client.say(context.message.author.mention + ' Level: ' + user.get_user_level())

    @commands.command(name='donate', aliases=['DONATE', 'GIVE', 'give'], pass_context=True)
    async def donate(self, context, amnt=None, receiver_string=None):
        # will automatically go to exception if all arguments weren't supplied correctly
        try:
            # not using *args[] array here, since there's only one correct syntax for using this command
            # create user instance with their discord ID, check database for their level field
            donator = Users(context.message.author.id)
            # use regex to extract only numbers from "receiver_string" to get their discord ID,
            # ex: <@348195501025394688> to 348195501025394688
            receiver = Users(re.findall("\d+", receiver_string)[0])

            # check if both users have accounts
            if receiver.find_user() == 0 or donator.find_user() == 0:
                await self.client.say(context.message.author.mention +
                                      " Either you or the target doesn't have an account."
                                      "\nUse **%create** to make one.")
                return
            # check if they have enough money for the donation
            # pass 0 to return integer version of money, see USERS.PY function
            if int(amnt) > donator.get_user_money(0):
                await self.client.say(context.message.author.mention +
                                      " You don't have enough money for that donation..."
                                      " <a:pepehands:485869482602922021> ")
                return

            # pass the donation amount, pass the receiver user object, and pass the receiver's string name
            msg = donator.donate_money(int(amnt), receiver, receiver_string)
            await self.client.say(msg)
        except:
            await self.client.say('Use %donate like so: **%donate X @user**    -- X being amount to donate')

def setup(client):
    client.add_cog(Account(client))
