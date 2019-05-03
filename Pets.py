#!/usr/bin/env python3
import random
import asyncio
import re
import discord
from discord.ext import commands
from Users import Users
from profanityfilter import ProfanityFilter
from random import choices


# short decorator function declaration, confirm that command user has an account in database
def has_account():
    def predicate(ctx):
        user = Users(ctx.message.author.id)
        if user.find_user() == 0:
            return False
        else:
            return True
    return commands.check(predicate)

class Pets:
    def __init__(self, client):
        self.client = client

    '''ADOPT A PET FUNCTION'''
    @has_account()
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(name='adopt', description='adopt a pet and raise it for rewards', brief='can use =adopt',
                      aliases=['ADOPT'], pass_context=True)
    async def adopt_pet(self, context):
        # create instance of the user who wishes to feed their pet
        pet_owner = Users(context.message.author.id)

        intro_msg = 'Welcome to the **Pet Shelter**!\n\nPlease enter your desired pet name now:'
        # embed intro message, then overwrite the variable with the actual message object
        em = discord.Embed(description=intro_msg, colour=0x607d4a)
        em.set_thumbnail(url="https://cdn.discordapp.com/emojis/560065150489722880.png?size=128")
        await self.client.say(embed=em)

        # wait for user's pet name entry
        pet_name = await self.client.wait_for_message(author=context.message.author, timeout=60)
        # remove everything except alphanumerics from the user's pet name entry
        pet_name = re.sub(r'\W+', '', pet_name.clean_content)

        # create an object to scan profanity
        pf = ProfanityFilter()
        # while the pet name entry has profanity, prompt user to re-enter a name
        while not pf.is_clean(pet_name):
            await self.client.say("Pet name has profanity! Please enter a new one now:")
            # wait for user's new pet name entry
            pet_name = await self.client.wait_for_message(author=context.message.author, timeout=60)
            # remove everything except alphanumerics from the user's pet name entry
            pet_name = re.sub(r'\W+', '', pet_name.clean_content)

        adoption_msg = pet_owner.add_pet(pet_name[:15])
        # embed confirmation message, then overwrite the variable with the actual message object
        em = discord.Embed(description=adoption_msg, colour=0x607d4a)
        em.set_thumbnail(url="https://cdn.discordapp.com/emojis/563872560308289536.png?v=1")
        await self.client.say(embed=em)

    '''FEED PET FUNCTION'''
    @has_account()
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(name='feed', description='feed your pet for XP', brief='can use =feed',
                      aliases=['FEED'], pass_context=True)
    async def feed(self, context):
        # create instance of the user who wishes to feed their pet
        pet_owner = Users(context.message.author.id)
        # retrieve pet name
        pet_name = pet_owner.get_user_pet_name()
        # "feed" the pet by updating the pet's xp, then place updated xp in a variable
        new_pet_xp = pet_owner.update_user_pet_xp()
        # retrieve integer of pet's current level
        pet_level = pet_owner.get_user_pet_level(0)

        # calculate the current level up requirement for the user's pet
        level_up_cost = int(300 * ((pet_level + 1) ** 1.18) - (300 * pet_level))
        if new_pet_xp >= level_up_cost:
            new_pet_level = pet_owner.update_user_pet_level()
            confirmation_msg = "Fed **" + pet_name + "**. They leveled up and transformed!\n" \
                                                     " They now have a higher chance to hunt for gear upgrades!" \
                                                     "\n\n\nNew level: **" + str(new_pet_level) + "**"
            if new_pet_level == 2:
                pet_avatar = "https://cdn.discordapp.com/emojis/491930617823494147.png?v=1"
            elif new_pet_level == 3:
                pet_avatar = "https://cdn.discordapp.com/emojis/400690504104148992.png?v=1"
            elif new_pet_level == 4:
                pet_avatar = "https://cdn.discordapp.com/emojis/400681095009533962.png?v=1"
            else:
                pet_avatar = "https://cdn.discordapp.com/emojis/422845006232027147.png?v=1"

        else:
            if pet_level == 1:
                pet_avatar = "https://cdn.discordapp.com/emojis/563872560308289536.png?v=1"
            elif pet_level == 2:
                pet_avatar = "https://cdn.discordapp.com/emojis/491930617823494147.png?v=1"
            elif pet_level == 3:
                pet_avatar = "https://cdn.discordapp.com/emojis/400690504104148992.png?v=1"
            elif pet_level == 4:
                pet_avatar = "https://cdn.discordapp.com/emojis/400681095009533962.png?v=1"
            else:
                pet_avatar = "https://cdn.discordapp.com/emojis/422845006232027147.png?v=1"

            confirmation_msg = "Fed **" + pet_name + "**! They feel stuffed for today." \
                                                     "\n\n\n**XP:** " + str(new_pet_xp) + "/" + str(level_up_cost)

        # embed confirmation message, then overwrite the variable with the actual message object
        em = discord.Embed(description=confirmation_msg, colour=0x607d4a)
        em.set_thumbnail(url=pet_avatar)
        await self.client.say(embed=em)

    '''FEED PET FUNCTION'''

    @has_account()
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(name='pet', description='check your pet status', brief='can use =pet',
                      aliases=['PET', 'Pet'], pass_context=True)
    async def pet_profile(self, context):
        # create instance of the user who wishes to feed their pet
        pet_owner = Users(context.message.author.id)
        # retrieve pet name
        pet_name = pet_owner.get_user_pet_name()
        # retrieve integer of pet's current xp
        pet_xp = pet_owner.get_user_pet_xp(0)
        # retrieve integer of pet's current level
        pet_level = pet_owner.get_user_pet_level(0)

        # calculate the current level up requirement for the user's pet
        level_up_cost = int(300 * ((pet_level + 1) ** 1.20) - (300 * pet_level))

        if pet_level == 1:
            pet_avatar = "https://cdn.discordapp.com/emojis/563872560308289536.png?v=1"
        elif pet_level == 2:
            pet_avatar = "https://cdn.discordapp.com/emojis/491930617823494147.png?v=1"
        elif pet_level == 3:
            pet_avatar = "https://cdn.discordapp.com/emojis/400690504104148992.png?v=1"
        elif pet_level == 4:
            pet_avatar = "https://cdn.discordapp.com/emojis/400681095009533962.png?v=1"
        else:
            pet_avatar = "https://cdn.discordapp.com/emojis/422845006232027147.png?v=1"

        pet_details = "**" + pet_name + "** (Pet Profile) " \
                                                     "\n\n\n**Level: **" + str(pet_level) + \
                                                     "\n**XP:** " + str(pet_xp) + "/" + str(level_up_cost)

        # embed confirmation message, then overwrite the variable with the actual message object
        em = discord.Embed(description=pet_details, colour=0x607d4a)
        em.set_thumbnail(url=pet_avatar)
        await self.client.say(embed=em)


def setup(client):
    client.add_cog(Pets(client))


