#!/usr/bin/env python3
from discord.ext import commands
import asyncio
from Users import Users
from Database import Database

# short decorator function declaration, confirm that command user has an account in database
def has_account():
    def predicate(ctx):
        user = Users(ctx.message.author.id)
        if user.find_user() == 0:
            return False
        else:
            return True

    return commands.check(predicate)


help_msg = "<a:worryswipe:525755450218643496>" \
           " Pick an item number from **=shop** then use **=buy X**" \
           " <a:worryswipe:525755450218643496>"

class Shop:
    def __init__(self, client):
        self.client = client

    @has_account()
    @commands.cooldown(1, 33, commands.BucketType.user)
    @commands.command(name='shop', description='view daily shop',
                      brief='view the daily shop', aliases=['SHOP'], pass_context=True)
    async def shop(self, context):
        # connect to database file
        db = Database(0)
        db.connect()
        # get list of current shop items from database
        daily_items = db.get_shop_list()
        string = "\n<a:worryhead:525164940231704577> **Daily Shop** <a:worryhead:525164940231704577>\n"

        # for each item retreived from database, get the details of each one from the returned tuple
        for item in daily_items:
            item_id = item[0]
            item_name = item[1]
            item_type = item[2]
            item_lvl = item[3]
            item_price = item[4]

            if item_type == 'weapon':
                item_type = '<:weapon1:532252764097740861>'
            elif item_type == 'helmet':
                item_type = '<:helmet2:532252796255469588>'
            elif item_type == 'chest':
                item_type = '<:chest5:532255708679503873>'
            elif item_type == 'boots':
                item_type = '<:boots1:532252814953676807>'


            string += ("**Item " + str(item_id) + "**: " + item_name +
                       " (**Lvl " + str(item_lvl) + "**)\n              __Type__: " +
                       item_type + "\n              __Price__: **$" + str(item_price) + "**\n")
        string += "\n" + help_msg

        msg = await self.client.say(string)
        # wait X seconds then delete the shop list message to reduce channel clutter
        await asyncio.sleep(30)
        await self.client.delete_message(msg)

    @has_account()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name='buy', description='buy an item from the daily shop',
                      brief='buy an item from the shop', aliases=['BUY'], pass_context=True)
    async def buy(self, context, *args):
        # connect to database file
        db = Database(0)
        db.connect()

        # try to retrieve the item number the user should have provided as a parameter
        try:
            item_id = int(args[0])
        except:
            await self.client.say(context.message.author.mention + " " + help_msg)
            return

        # get the specified item's stats from the database
        item = db.get_shop_item(item_id)
        # if the specified item number isn't in the Shop table in the database,
        # inform user to check the daily shop again because item doesn't exist and return
        if not item:
            await self.client.say("<:worrymag1:531214786646507540> Couldn't find that item "
                                  "<:worrymag2:531214802266095618>\nCheck **=shop** again...")
            return

        # make variables for all the details on the specified item
        item_name = item[1]
        item_type = item[2]
        item_lvl = item[3]
        item_price = item[4]
        # create instance of user
        user = Users(context.message.author.id)

        # if user doesn't have enough money for the specified item, inform user how much more money they need + return
        if user.get_user_money(0) < item_price:
            difference = str(item_price - user.get_user_money(0))
            await self.client.say("<:worrymag1:531214786646507540> Not enough money! You need **$" + difference +
                                  "** more for that item! <:worrymag2:531214802266095618>")
            return

        # if user's item level is already greater than or equal to the item the user is trying to buy, inform user + return
        # because the user should not be able to downgrade
        error_msg = "<:worrymag1:531214786646507540> Your current equipped item is already **better or equal** to that! " \
                    "<:worrymag1:531214786646507540>"
        # retrieve the first four values [0-3] returned from get_user_battle_stats and store them into variables
        user_weapon_lvl, user_helmet_lvl, user_chest_lvl, user_boots_lvl = user.get_user_battle_stats(0)[0:4]
        # compare user's item level against specified item's level, based off item type the user is trying to purchase
        if item_type == 'weapon':
            if user_weapon_lvl >= item_lvl:
                await self.client.say(error_msg)
                return
        elif item_type == 'helmet':
            if user_helmet_lvl >= item_lvl:
                await self.client.say(error_msg)
                return
        elif item_type == 'chest':
            if user_chest_lvl >= item_lvl:
                await self.client.say(error_msg)
                return
        elif item_type == 'boots':
            if user_boots_lvl >= item_lvl:
                await self.client.say(error_msg)
                return

        msg = await self.client.say("Type **confirm** to buy:\n\n__" + item_name +
                                    "__ (**Lvl " + str(item_lvl) + "**)\n              __Type__: " +
                                    item_type + "\n              __Price__: **$" + str(item_price) + "**\n")

        # wait for a "confirm" response from the user to process the purchase
        # if it is not "confirm", cancel transaction
        response = await self.client.wait_for_message(author=context.message.author, timeout=30)
        if response.clean_content.upper() == 'CONFIRM':
            # subtract the item's price from user's bank account
            await self.client.say("<:worrysign10:531221748964786188> Bought **" + item_name
                                  + "**! <:worrysign10:531221748964786188>\n" + user.update_user_money(item_price * -1))
            # update user's item level for that item type bought
            await self.client.say(user.update_user_battle_gear(item_type, item_lvl))
        else:
            await self.client.say(context.message.author.mention + ' Cancelled purchase!')

        # clean up messages to reduce spam in channel
        await self.client.delete_message(response)
        await self.client.delete_message(msg)


def setup(client):
    client.add_cog(Shop(client))
