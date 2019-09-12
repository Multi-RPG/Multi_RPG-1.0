#!/usr/bin/env python3
from Database import Database

# This class serves as a medium between the front-end bot code and the back-end database class
# Performs string or data manipulation as well, so database class can be as simple as possible


class Users:
    def __init__(self, id):
        self.id = id

    def add_user(self):
        hm_db = Database(self.id)
        hm_db.connect()
        return (
            " Made account!\nYour starting :moneybag: balance: **$"
            + str(hm_db.insert_acct())
            + "**"
        )

    def add_pet(self, pet_name):
        hm_db = Database(self.id)
        hm_db.connect()
        hm_db.insert_pet(pet_name)
        return (
            " Adopted **"
            + pet_name
            + "**!\n\nYou can: \n1. Use **=feed** to level them up\n"
            "2. Use **=hunt** for rewards\n"
            "3. Use **=pet** to check their status"
        )

    def find_user(self):
        hm_db = Database(self.id)
        hm_db.connect()
        return hm_db.find_acct()

    def find_pet(self):
        hm_db = Database(self.id)
        hm_db.connect()
        return hm_db.find_pet()

    def delete_user(self):
        hm_db = Database(self.id)
        hm_db.connect()
        hm_db.delete_acct()
        return " Deleted account! <a:pepehands:485869482602922021>"

    def donate_money(self, amnt, receiver, receiver_string):
        self.update_user_money(amnt * -1)
        receiver.update_user_money(amnt)
        return " donated **$" + str(amnt) + "** to " + receiver_string

    # pass 0 to 'string' to return integer version of user's money EX: 100, default is string, EX: "**$100**"
    def get_user_money(self, string=1):
        hm_db = Database(self.id)
        hm_db.connect()

        # if we want integer form of money
        if string == 0:
            return hm_db.get_money()
        # if we want the full bold discord-formatted string sequence of money
        elif string == 1:
            # format money for commas and bold
            return "**$" + str("{:,}".format(hm_db.get_money())) + "**"

    # pass 0 to 'string' to return integer version of user's level EX: 3, default is string, EX: "**3**"
    def get_user_level(self, string=1):
        hm_db = Database(self.id)
        hm_db.connect()

        # if we want integer form of level
        if string == 0:
            return hm_db.get_level()
        # if we want the full bold discord-formatted string sequence of user level
        elif string == 1:
            return "**" + str(hm_db.get_level()) + "**"

    def get_user_pet_name(self, string=1):
        hm_db = Database(self.id)
        hm_db.connect()
        return hm_db.get_pet_name()

    # pass 0 to 'string' to return integer version of user's pet xp EX: 3, default is string, EX: "**3**"
    def get_user_pet_xp(self, string=1):
        hm_db = Database(self.id)
        hm_db.connect()

        # if we want integer form of pet level
        if string == 0:
            return hm_db.get_pet_xp()
        # if we want the full bold discord-formatted string sequence of user's pet xp
        elif string == 1:
            return "**" + str(hm_db.get_pet_xp()) + "**"

    # pass 0 to 'string' to return integer version of user's pet level EX: 3, default is string, EX: "**3**"
    def get_user_pet_level(self, string=1):
        hm_db = Database(self.id)
        hm_db.connect()

        # if we want integer form of pet level
        if string == 0:
            return hm_db.get_pet_level()
        # if we want the full bold discord-formatted string sequence of user's pet level
        elif string == 1:
            return "**" + str(hm_db.get_pet_level()) + "**"

    def get_user_peace_status(self):
        hm_db = Database(self.id)
        hm_db.connect()

        return hm_db.get_peace_status()

    def get_user_peace_cooldown(self):
        hm_db = Database(self.id)
        hm_db.connect()

        return hm_db.get_peace_cooldown()

    # returns integer of user's weapon + helmet + chest + boots levels' total
    def get_user_item_score(self):
        hm_db = Database(self.id)
        hm_db.connect()

        return hm_db.get_item_score()

    # pass 0 to 'string' to return integer version of user's battles records EX: 3, default is string, EX: "**3**"
    # this will function as a collective pull of all the user's details
    def get_user_stats(self, string=1):
        hm_db = Database(self.id)
        hm_db.connect()

        # if we want integer form of each battle record
        if string == 0:
            return hm_db.get_battle_stats()
        # if we want the full formatted string sequence of battle records
        elif string == 1:
            # assign each variable from the sql query
            weapon_level, helmet_level, chest_level, boots_level, battles_lost, battles_won, total_winnings = (
                hm_db.get_battle_stats()
            )
            total_winnings = "{:,}".format(total_winnings)
            user_level = hm_db.get_level()
            # format money with commas
            user_money = "{:,}".format(hm_db.get_money())

            # add full bold discord-format to each variable
            item_score = (
                "**"
                + str(weapon_level + helmet_level + chest_level + boots_level)
                + "**"
            )

            weapon_level = "**" + str(weapon_level) + "**"
            helmet_level = "**" + str(helmet_level) + "**"
            chest_level = "**" + str(chest_level) + "**"
            boots_level = "**" + str(boots_level) + "**"
            battles_lost = "**" + str(battles_lost) + "**"
            battles_won = "**" + str(battles_won) + "**"
            total_winnings = "**$" + str(total_winnings) + "**"
            user_level = "**" + str(user_level) + "**"
            user_money = "**$" + str(user_money) + "**"

            # have to insert encode \u200B for spaces when using discord encoding
            return (
                "\n**ACCOUNT:**"
                "\n:chart_with_upwards_trend: Level: \u200B \u200B \u200B \u200B \u200B \u200B"
                + user_level
                + "\n:moneybag: Money: \u200B \u200B"
                + user_money
                + "\n\n**GEAR:**"
                "\n<:weapon1:532252764097740861> Weapon: \u200B \u200B"
                + weapon_level
                + "\n<:helmet2:532252796255469588> Helmet: \u200B \u200B \u200B \u200B"
                + helmet_level
                + "\n<:chest5:532255708679503873> Chest: \u200B \u200B \u200B \u200B \u200B \u200B \u200B"
                + chest_level
                + "\n<:boots1:532252814953676807> Boots: \u200B \u200B \u200B \u200B \u200B \u200B \u200B"
                + boots_level
                + "\n__Total__:\u200B \u200B \u200B"
                + item_score
                + "\n\n**TOURNAMENT RECORDS:**"
                "\n:crossed_swords:\u200B \u200B lost: \u200B \u200B"
                + battles_lost
                + "\n:crossed_swords:\u200B \u200B won: "
                + battles_won
                + "\n__Total winnings__: "
                + total_winnings
            )

    def get_user_ticket_status(self):
        hm_db = Database(self.id)
        hm_db.connect()
        return hm_db.get_ticket_status()

    def get_user_ranks(self):
        hm_db = Database(self.id)
        hm_db.connect()
        rankings = hm_db.get_ranks()

        return rankings

    # this function calls the Database function to add amount to bank account
    def update_user_money(self, amount):
        hm_db = Database(self.id)
        hm_db.connect()
        return (
            "Your new account balance: **$"
            + str("{:,}".format(hm_db.update_money(amount)))
            + "**"
        )

    def update_user_level(self):
        hm_db = Database(self.id)
        hm_db.connect()
        return (
            "\n<:worrysign10:531221748964786188> New level: **"
            + str(hm_db.update_level())
            + "** <:worrysign10:531221748964786188>"
        )

    def update_user_pet_xp(self):
        hm_db = Database(self.id)
        hm_db.connect()

        return hm_db.update_pet_xp()

    def update_user_pet_level(self):
        hm_db = Database(self.id)
        hm_db.connect()

        return hm_db.update_pet_level()

    # enables the peace status to "1", so users cannot =rob @target a user
    def toggle_user_peace_status(self):
        hm_db = Database(self.id)
        hm_db.connect()

        return hm_db.toggle_peace_status()

    # enables the peace cooldown to "1", so user cannot exit peace mode until reset
    def update_user_peace_cooldown(self):
        hm_db = Database(self.id)
        hm_db.connect()

        return hm_db.update_peace_cooldown()

    def update_user_battle_gear(self, gear_type, level):
        hm_db = Database(self.id)
        hm_db.connect()

        if gear_type == "weapon":
            return (
                " Your new total item score: **"
                + str(hm_db.update_battle_weapon(level))
                + "**"
            )
        elif gear_type == "helmet":
            return (
                " Your new total item score: **"
                + str(hm_db.update_battle_helmet(level))
                + "**"
            )
        elif gear_type == "chest":
            return (
                " Your new total item score: **"
                + str(hm_db.update_battle_chest(level))
                + "**"
            )
        elif gear_type == "boots":
            return (
                " Your new total item score: **"
                + str(hm_db.update_battle_boots(level))
                + "**"
            )

    def update_user_tourney_server_id(self, server_name, server_id):
        hm_db = Database(self.id)
        hm_db.connect()

        hm_db.update_tourney_server_id(server_id)
        return (
            ":crossed_swords: Registered for **"
            + server_name
            + "** daily FFA tournament! :crossed_swords:"
            + "\nResults will be live by :alarm_clock: **7 AM PST!**"
        )

    def update_user_records(self, battles_lost, battles_won, total_winnings):
        hm_db = Database(self.id)
        hm_db.connect()

        return (
            " Your new battle records: **"
            + str(
                hm_db.update_battle_records(battles_lost, battles_won, total_winnings)
            )
            + "**"
        )

    def update_user_lottery_guess(self, ticket_guess, ticket_active):
        hm_db = Database(self.id)
        hm_db.connect()

        hm_db.update_lottery_guess(ticket_guess, ticket_active)
        return (
            "Thanks! Processed ticket ID: **"
            + self.id
            + "**\n "
            + "Results will be live by :alarm_clock: **7 AM PST!**"
        )
