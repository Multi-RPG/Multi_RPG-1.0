#!/usr/bin/env python3
from discord.ext import commands
 
class Utilities:
    def __init__(self, client):
        self.client = client

    @commands.cooldown(1,  5, commands.BucketType.user)
    @commands.command(name='clear', description='Deletes messages in the channel.',
                      brief='can use "%clear" or "%clear X", with X being #  messages to delete',
                      aliases=['c', 'clr', 'CLEAR', 'C', 'CLR', 'clean', 'CLEAN'], pass_context=True)
    async def clear(self, context, *args):
        counter = 0
        # try-catch block, because of *args array. if no argument given in discord after "%clear", it will go to the exception
        try:
            async for msg in self.client.logs_from(context.message.channel):
                if counter <= int(args[0]): # the argument is passed as string, gotta cast
                    await self.client.delete_message(msg)
                    counter += 1
            await self.client.say('Cleared ' + args[0] + ' messages...')
        except:
            async for msg in self.client.logs_from(context.message.channel):
                if counter <= int(1): # default to delete 1 message if they didn't specify how many to delete
                    await self.client.delete_message(msg)
                    counter += 1        
            await self.client.say('Cleared 1 message... '
                                  'Use **%clear X** to clear a higher, specified amount.')

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='code', description='Give link to code', brief='can use "%code',
                      aliases=['CODE'], pass_context=True)
    async def source_code_link(self, context):
        await self.client.say('Code for this **open-source** '
                              'bot: https://github.com/jdkennedy45/Discord-Bot')

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='invite', description='Give link to code', brief='can use "%code',
                      aliases=['link', 'botlink', 'invitelink'], pass_context=True)
    async def invite_link(self, context):
        # embed link in <> so discord will disable "link preview embedding"
        await self.client.say('Invite link for this **open-source** bot: \n'
                              '<https://discordapp.com/oauth2/authorize?client_id='
                              '486349031224639488&permissions=8&scope=bot>')

def setup(client):
    client.add_cog(Utilities(client))