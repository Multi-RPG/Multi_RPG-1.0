#!/usr/bin/env python3
import re
from Db import Db
 
class Users:
    def __init__(self, id):
        self.id = id

    def add_user(self):
        hm_db = Db(self.id)
        hm_db.connect()
        # new user will start off with level 1, and $50
        return hm_db.insert_acct(1, 50)

    def update_user_money(self, amount):
        hm_db = Db(self.id)
        hm_db.connect()
        return hm_db.update_money(amount)
        
    def find_user(self):
        hm_db = Db(self.id)
        hm_db.connect()
        return hm_db.find_acct()

    # pass 0 to 'string' to return integer version of user's money EX: 100, default is string, EX: "**$100**"
    def get_user_money(self, string=1):
        hm_db = Db(self.id)
        hm_db.connect()
        
        # if we want integer form of money
        if string == 0:
            # regex for only retrieving numbers from the string that the db function returns
            return int(re.findall("\d+", hm_db.get_money())[0])
        elif string == 1:
            return hm_db.get_money()

    # pass 0 to 'string' to return integer version of user's level EX: 3, default is string, EX: "Level: **3**"
    def get_user_level(self, string=1):
        hm_db = Db(self.id)
        hm_db.connect()

        # if we want integer form of level
        if string == 0:
            # regex for only retrieving numbers from the string that the db function returns
            return int(re.findall("\d+", hm_db.get_level())[0])
        elif string == 1:
            return hm_db.get_level()
            
    def delete_user(self):
        hm_db = Db(self.id)
        hm_db.connect()
        return hm_db.delete_acct()

    def donate_money(self, amnt, receiver, receiver_string):
        self.update_user_money(amnt*-1)
        receiver.update_user_money(amnt)
        return " Donated **$" + str(amnt) + "** to " + receiver_string
