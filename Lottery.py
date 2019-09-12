#!/usr/bin/env python3
import asyncio
import discord
from discord.ext import commands
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


class Lottery:
    def __init__(self, client):
        self.client = client

    """ENTER LOTTERY FUNCTION"""

    @has_account()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(
        name="lotto",
        description="Enter the daily lottery.",
        brief="can use =lotto",
        aliases=["LOTTO", "lottery", "LOTTERY"],
        pass_context=True,
    )
    async def enter_lottery(self, context):
        # create instance of the user entering the lotto
        entry = Users(context.message.author.id)
        # if they already got a ticket today, don’t let them overwrite it
        if entry.get_user_ticket_status() == 2 or entry.get_user_ticket_status() == 1:
            error_msg = await self.client.say(
                "**ERROR!** You have already entered a **lottery** today!"
                "<a:worryhead:525164940231704577>"
            )
            await asyncio.sleep(8)
            await self.client.delete_message(error_msg)
            await self.client.delete_message(context.message)
            return

        intro_msg = "Welcome to the **Basic** Lotto!\n Please enter your **ticket guess** now (1-5):"
        # embed intro message, then overwrite the variable with the actual message object
        em = discord.Embed(description=intro_msg, colour=0x607D4A)
        em.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/525164940231704577.gif?size=40"
        )
        intro_msg = await self.client.say(embed=em)

        # wait for user's ticket guess
        guess = await self.client.wait_for_message(
            author=context.message.author, timeout=60
        )

        if not guess.clean_content.isdigit():
            cancel_msg = await self.client.say("**Cancelled** lottery entry!")
            await asyncio.sleep(7)
            await self.client.delete_message(intro_msg)
            await self.client.delete_message(cancel_msg)
            return

        # next loop may be redundant, but you can never know what your end-users will do
        counter = 0
        while not 5 >= int(guess.clean_content) >= 1:
            counter += 1
            # give them 3 attempts to input a 1-5 integer
            if counter == 3:
                return
            # delete their incorrect number guess
            await self.client.delete_message(guess)
            # prompt for valid number
            retry_msg = await self.client.say("Please enter an integer (1-5):")
            # wait for user's ticket guess
            guess = await self.client.wait_for_message(
                author=context.message.author, timeout=60
            )
            # delete retry prompt
            await self.client.delete_message(retry_msg)

        confirm_msg = entry.update_user_lottery_guess(guess.clean_content, 1)
        # embed intro message, then overwrite the variable with the actual message object
        em = discord.Embed(description=confirm_msg, colour=0x607D4A)
        em.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/518016461604913162.gif?size=40"
        )
        await self.client.say(embed=em)
        # wait 10 seconds, then clean up bot's spam
        await asyncio.sleep(10)
        await self.client.delete_message(guess)
        await self.client.delete_message(intro_msg)

    """ENTER PREMIUM LOTTERY FUNCTION"""

    @has_account()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(
        name="lotto2",
        description="Enter the daily lottery as a premium ticket.",
        brief="can use =lotto2",
        aliases=["LOTTO2", "lottery2", "LOTTERY2"],
        pass_context=True,
    )
    async def enter_lottery2(self, context):
        # create instance of the user entering the lotto
        entry = Users(context.message.author.id)
        entry_fee = entry.get_user_level(0) * 10
        # if they already got a ticket today, don’t let them overwrite it
        if entry.get_user_ticket_status() == 2 or entry.get_user_ticket_status() == 1:
            error_msg = await self.client.say(
                "**ERROR!** You have already entered a **lottery** today!"
                "<a:worryhead:525164940231704577>"
            )
            await asyncio.sleep(8)
            await self.client.delete_message(error_msg)
            await self.client.delete_message(context.message)
            return

        if entry.get_user_money(0) < entry_fee:
            error_msg = await self.client.say(
                "**ERROR!** You do not have **$"
                + str(entry_fee)
                + "** to enter the premium lottery..."
                + " Use =lotto for the free lotto <a:worryhead:525164940231704577>"
            )
            await asyncio.sleep(8)
            await self.client.delete_message(error_msg)
            await self.client.delete_message(context.message)
            return

        intro_msg = (
            "Welcome to the **Premium** Lotto! _(Your ticket will cost **$"
            + str(entry_fee)
            + "**)_ \nPlease enter your **ticket guess** now (1-5):"
        )

        # embed intro message, then overwrite the variable with the actual message object
        em = discord.Embed(description=intro_msg, colour=0x607D4A)
        em.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/525164940231704577.gif?size=40"
        )
        intro_msg = await self.client.say(embed=em)

        # wait for user's ticket guess
        guess = await self.client.wait_for_message(
            author=context.message.author, timeout=60
        )

        if not guess.clean_content.isdigit():
            cancel_msg = await self.client.say("Cancelled lottery entry!")
            await asyncio.sleep(8)
            await self.client.delete_message(intro_msg)
            await self.client.delete_message(cancel_msg)
            return

        # next loop may be redundant, but you can never know what your end-users will do
        counter = 0
        while not 5 >= int(guess.clean_content) >= 1:
            counter += 1
            # give them 3 attempts to input a 1-5 integer
            if counter == 3:
                return
            # delete their incorrect number guess
            await self.client.delete_message(guess)
            # prompt for valid number
            retry_msg = await self.client.say("Please enter an integer (1-5):")
            # wait for user's ticket guess
            guess = await self.client.wait_for_message(
                author=context.message.author, timeout=60
            )
            # delete retry prompt
            await self.client.delete_message(retry_msg)

        # take the entry fee for premium lottery
        entry.update_user_money(-entry_fee)
        # register a premium ticket (ticket_active = 2)
        confirm_msg = entry.update_user_lottery_guess(guess.clean_content, 2)
        # embed intro message, then overwrite the variable with the actual message object
        em = discord.Embed(description=confirm_msg, colour=0x607D4A)
        em.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/518016461604913162.gif?size=40"
        )
        await self.client.say(embed=em)
        # wait 10 seconds, then clean up bot's spam
        await asyncio.sleep(10)
        await self.client.delete_message(guess)
        await self.client.delete_message(intro_msg)


def setup(client):
    client.add_cog(Lottery(client))
