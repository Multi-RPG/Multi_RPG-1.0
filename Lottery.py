#!/usr/bin/env python3
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

    '''ENTER LOTTERY FUNCTION'''
    @has_account()
    @commands.cooldown(1, 500, commands.BucketType.user)
    @commands.command(name='lotto', description='Enter the daily lottery.', brief='can use =lotto',
                      aliases=['LOTTO', 'lottery', 'LOTTERY'], pass_context=True)
    async def enter_lottery(self, context):
        # create instance of the user entering the lotto
        entry = Users(context.message.author.id)

        await self.client.say('<a:worryhead:525164940231704577> Welcome to the Lotto! <a:worryhead:525164940231704577>\n'
                              ' Please enter your **ticket guess** now (1-5):')
        guess = await self.client.wait_for_message(author=context.message.author,
                                                   timeout=60)  # wait for user's ticket guess

        counter = 0
        while not guess.clean_content.isdigit():
            # only give 3 tries to input a valid integer digit
            counter += 1
            if counter == 3:
                return
            await self.client.say('Please enter your **ticket guess** again, as an integer (1-5):')
            guess = await self.client.wait_for_message(author=context.message.author,
                                                       timeout=60)  # wait for user's ticket guess

        # next loop may be redundant, but you can never know what your end-users will do
        # check if the digit is 1-5
        while not 5 >= int(guess.clean_content) >= 1:
            counter += 1
            if counter == 3:
                return
            await self.client.say('Please enter your **ticket guess** again, as an integer (1-5):')
            guess = await self.client.wait_for_message(author=context.message.author,
                                                       timeout=60)  # wait for user's ticket guess

        # update their ticket_guess in the database with their new guess
        await self.client.say(entry.update_user_lottery_guess(guess.clean_content))

def setup(client):
    client.add_cog(Lottery(client))