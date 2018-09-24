#!/usr/bin/env python3
import asyncio
from discord.ext import commands
 
class Utilities:
    def __init__(self, client):
        self.client = client

    @commands.cooldown(1,  15, commands.BucketType.user)
    @commands.command(name='clear', description='Deletes messages in the channel.',
                      brief='can use "=clear" or "=clear X", with X being #  messages to delete',
                      aliases=['c', 'clr', 'CLEAR', 'C', 'CLR', 'clean', 'CLEAN'], pass_context=True)
    async def clear(self, context, *args):
        # try-catch block, because of *args array. if no argument given in discord after "=clear", it will go to the exception
        try:
            deleted = await self.client.purge_from(context.message.channel, limit=int(args[0]))
            await self.client.say("Deleted %s message(s)" % str(len(deleted)))

        except:
            await self.client.purge_from(context.message.channel, limit=1)
            await self.client.say('Cleared 1 message... '
                                  'Use **=clear X** to clear a higher, specified amount.')

    @commands.command(name='id', aliases=['myid', 'ID'], pass_context=True)
    async def discordID(self, context):
        await self.client.say(context.message.author.mention + ' Your discord ID: **' + context.message.author.id + '**')

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='code', description='Give link to code', brief='can use "=code',
                      aliases=['CODE'], pass_context=True)
    async def source_code_link(self, context):
        await self.client.say('Code for this **open-source** '
                              'bot: https://github.com/jdkennedy45/Discord-Bot')

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='invite', description='Give link to code', brief='can use "=code',
                      aliases=['link', 'botlink', 'invitelink'], pass_context=True)
    async def invite_link(self, context):
        # embed link in <> so discord will disable "link preview embedding"
        await self.client.say('Invite link for this **open-source** bot: \n'
                              '<https://discordapp.com/oauth2/authorize?client_id='
                              '486349031224639488&permissions=8&scope=bot>')

def setup(client):
    client.add_cog(Utilities(client))
