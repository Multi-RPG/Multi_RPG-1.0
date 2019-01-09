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
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name='lotto', description='Enter the daily lottery.', brief='can use =lotto',
                      aliases=['LOTTO', 'lottery', 'LOTTERY'], pass_context=True)
    async def enter_lottery(self, context):
        # create instance of the user entering the lotto
        entry = Users(context.message.author.id)
        # if they already purchased a premium ticket, don’t let them overwrite it by mistake with a free ticket
        if entry.get_user_ticket_status() == 2:
            await self.client.say('**ERROR!** You have already entered and paid your entry fee'
                                  ' for the **premium lottery** today! <a:worryhead:525164940231704577>')
            return
            
        await self.client.say('<a:worryhead:525164940231704577> Welcome to the **Basic** Lotto!'
                              ' <a:worryhead:525164940231704577>\n Please enter your **ticket guess** now (1-5):')

        guess = await self.client.wait_for_message(author=context.message.author,
                                                   timeout=60)  # wait for user's ticket guess

        if not guess.clean_content.isdigit():
            await self.client.say('Cancelled lottery entry!')
            return

        # next loop may be redundant, but you can never know what your end-users will do
        counter = 0
        while not 5 >= int(guess.clean_content) >= 1:
            counter += 1
            # give them 3 attempts to input a 1-5 integer
            if counter == 3:
                return
            await self.client.say('Please enter your **ticket guess** again, as an integer (1-5):')
            guess = await self.client.wait_for_message(author=context.message.author,
                                                       timeout=60)  # wait for user's ticket guess

        await self.client.say(entry.update_user_lottery_guess(guess.clean_content, 1))

    '''ENTER PREMIUM LOTTERY FUNCTION'''
    @has_account()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name='lotto2', description='Enter the daily lottery as a premium ticket.', brief='can use =lotto2',
                      aliases=['LOTTO2', 'lottery2', 'LOTTERY2'], pass_context=True)
    async def enter_lottery2(self, context):
        # create instance of the user entering the lotto
        entry = Users(context.message.author.id)
        entry_fee = entry.get_user_level(0) * 17
        # if they already purchased a premium ticket, don’t let them overwrite it by mistake by purchasing another one
        if entry.get_user_ticket_status() == 2:
            await self.client.say('**ERROR!** You have already entered and paid your $**' + str(entry_fee) + '** entry'
                                  ' for the **premium lottery** today! <a:worryhead:525164940231704577>')
            return

                
        if entry.get_user_money(0) < entry_fee:
            await self.client.say('**ERROR!** You do not have **$' + str(entry_fee) +'** to enter the premium lottery...'
                                  ' Use =lotto for the free lotto <a:worryhead:525164940231704577>')
            return
        await self.client.say('<a:worryhead:525164940231704577> Welcome to the **Premium** Lotto! '
                              '<a:worryhead:525164940231704577> _(Your ticket will cost **$' + str(entry_fee) + '**)_ \n'
                              ' Please enter your **ticket guess** now (1-5):')
        guess = await self.client.wait_for_message(author=context.message.author,
                                                   timeout=60)  # wait for user's ticket guess

        if not guess.clean_content.isdigit():
            await self.client.say('Cancelled lottery entry!')
            return

        # next loop may be redundant, but you can never know what your end-users will do
        counter = 0
        while not 5 >= int(guess.clean_content) >= 1:
            counter += 1
            # give them 3 attempts to input a 1-5 integer
            if counter == 3:
                return
            await self.client.say('Please enter your **ticket guess** again, as an integer (1-5):')
            guess = await self.client.wait_for_message(author=context.message.author,
                                                       timeout=60)  # wait for user's ticket guess

        # take the entry fee for premium lottery
        entry.update_user_money(-entry_fee)
        await self.client.say(entry.update_user_lottery_guess(guess.clean_content, 2))


def setup(client):
    client.add_cog(Lottery(client))
