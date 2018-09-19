#!/usr/bin/env python3
import re
from Db import Db
 
class Users:
    def __init__(self, id):
        self.id = id

    def add_user(self):
        hm_db = Db(self.id)
        hm_db.connect()
        try:
            return " Made account!\nYour starting :moneybag: balance: **$" + str(hm_db.insert_acct()) + "**"

        # caught integrity error in the SQL statement, so that means account already exists
        except:
            return " You already have an account!!\nYour :moneybag: balance: " + self.get_user_money()

    def update_user_money(self, amount):
        hm_db = Db(self.id)
        hm_db.connect()
        try:
            return "Your new account balance: **$" + hm_db.update_money(amount) + "**"

        # caught error in the SQL statement, so that means no account was found
        except:
            return "\nYou have no bank account! <a:rotatethink:490228030556340259>\n" \
                   "Use **%create** to start one. "
        
    def find_user(self):
        hm_db = Db(self.id)
        hm_db.connect()
        return hm_db.find_acct()

    def delete_user(self):
        hm_db = Db(self.id)
        hm_db.connect()

        # first check if that user has an account
        # not using try/catch here since DELETE won't return any errors in SQL
        if self.find_user() == 0:
            return " You do not have an account to delete <a:rotatethink:490228030556340259>"
        else:
            hm_db.delete_acct()
            return " Deleted account! <a:pepehands:485869482602922021>"

    def donate_money(self, amnt, receiver, receiver_string):
        self.update_user_money(amnt * -1)
        receiver.update_user_money(amnt)
        return " Donated **$" + str(amnt) + "** to " + receiver_string

    # pass 0 to 'string' to return integer version of user's money EX: 100, default is string, EX: "**$100**"
    def get_user_money(self, string=1):
        hm_db = Db(self.id)
        hm_db.connect()

        try:
            # if we want integer form of money
            if string == 0:
                return hm_db.get_money()
            # if we want the full bold discord-formatted string sequence of money
            elif string == 1:
                return "**$" + str(hm_db.get_money()) + "**"

        # caught error in the SQL statement, so that means no account was found
        except:
            return "**$0**. \n\nNo bank account! <a:rotatethink:490228030556340259>\n" \
                   "Use **%create** to start one. "

    # pass 0 to 'string' to return integer version of user's level EX: 3, default is string, EX: "**3**"
    def get_user_level(self, string=1):
        hm_db = Db(self.id)
        hm_db.connect()

        try:
            # if we want integer form of money
            if string == 0:
                return hm_db.get_level()
            # if we want the full bold discord-formatted string sequence of money
            elif string == 1:
                return "**" + str(hm_db.get_level()) + "**"

        # caught error in the SQL statement, so that means no account was found
        except:
            return "**0**. \n\nNo bank account! <a:rotatethink:490228030556340259>\n" \
                   "Use **%create** to start one. "

    # pass 0 to 'string' to return integer version of user's battles records EX: 3, default is string, EX: "**3**"
    def get_user_battle_records(self, string=1):
        hm_db = Db(self.id)
        hm_db.connect()

        try:
            # if we want integer form of each battle record
            if string == 0:
                return hm_db.get_battle_records()
            # if we want the full formatted string sequence of battle records
            elif string == 1:
                # assign each variable from the sql query
                battles_lost, battles_won, total_winnings = hm_db.get_battle_records()
                # add full bold discord-format to each variable
                battles_lost = '**' + str(battles_lost) + '**'
                battles_won = '**' + str(battles_won) + '**'
                total_winnings = '**$' + str(total_winnings) + '**'

                return ('\n** **\n'
                ':crossed_swords:  lost: ' + battles_lost +
                '\n:crossed_swords:  won: ' + battles_won +
                '\nTotal winnings: ' + total_winnings)

        # caught error in the SQL statement, so that means no account was found
        except:
            return "\nNo bank account! <a:rotatethink:490228030556340259>\n" \
                   "Use **%create** to start one. "
