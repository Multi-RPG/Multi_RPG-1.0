#!/usr/bin/env python3
import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self, id):
        self.id = id

    def connect(self):
        try:
            self.connection = sqlite3.connect("db_and_words\hangman.db")
            # Next part required to enable foreign keys on sqlite. It must execute every connection.
            self.connection.execute("PRAGMA foreign_keys = ON")
            return self.connection
        except Error as e:
            print(e)

    def insert_acct(self):
        cur = self.connection.cursor()

        # new user will start off with level 1, $50 in bag and $0 in bank
        sql = "INSERT INTO Users(user_id, level, money, bank) VALUES(?, ?, ?, ?)"
        cur.execute(sql, (self.id, 1, 50, 0))

        # new user will start off with 0 battles lost, 0 battles won, and 0 total winnings
        sql = "INSERT INTO Battles(fighter_id, battles_lost, battles_won, total_winnings) VALUES(?, ?, ?, ?)"
        cur.execute(sql, (self.id, 0, 0, 0))

        sql = "INSERT INTO Lottery(ticket_id, ticket_guess, ticket_active) VALUES(?, ?, ?)"
        cur.execute(sql, (self.id, 99999999, 0))

        # print users table to console after inserts
        cur.execute("select * from Users")
        rows = cur.fetchall()
        print("\nUsers after insert: \n")
        for row in rows:
            print(row)

        self.connection.commit()
        return self.get_money()

    def insert_shop_item(self, name, type, level, price):
        cur = self.connection.cursor()

        sql = "INSERT INTO Shop(name, type, level, price) VALUES(?, ?, ?, ?)"
        cur.execute(sql, (name, type, level, price))

        # print users table to console after inserts
        cur.execute("select * from Shop")
        rows = cur.fetchall()
        print("\nShop after insert: \n")
        for row in rows:
            print(row)

        self.connection.commit()

    def find_acct(self):
        cur = self.connection.cursor()

        # test if the user ID exists in the datbase
        sql = "SELECT * FROM Users WHERE user_id = ?"
        cur.execute(sql, (self.id,))
        row = cur.fetchone()
        # see if a row exists in the fetch results, if not, they don't have an account
        try:
            if row[0] == "":
                pass
            # the above if statement didn't throw error, so the account exists. return 1
            return 1
        except:
            return 0

    def delete_acct(self):
        cur = self.connection.cursor()

        sql = "DELETE FROM Users WHERE user_id = ?"
        cur.execute(sql, (self.id,))
        cur.execute("select * from Users")
        rows = cur.fetchall()
        print("\nUsers after delete: \n")
        for row in rows:
            print(row)

        self.connection.commit()

    def get_money(self):
        cur = self.connection.cursor()

        sql = "SELECT money FROM Users WHERE user_id = ?"
        cur.execute(sql, (self.id,))
        row = cur.fetchone()
        return row[0]

    def get_bank_balance(self):
        cur = self.connection.cursor()

        sql = "SELECT bank FROM Users WHERE user_id = ?"
        cur.execute(sql, (self.id,))
        row = cur.fetchone()
        return row[0]

    def get_level(self):
        cur = self.connection.cursor()

        sql = "SELECT level FROM Users WHERE user_id = ?"
        cur.execute(sql, (self.id,))
        row = cur.fetchone()
        return row[0]

    def get_battle_stats(self):
        cur = self.connection.cursor()

        sql = "SELECT weapon_level, helmet_level, chest_level, boots_level, " \
              "battles_lost, battles_won, total_winnings FROM Battles WHERE fighter_id = ?"
        cur.execute(sql, (self.id,))
        row = cur.fetchone()
        # fetchone() returns only 1 row, and not in tuple format like fetchall()
        # now we can just use array indexes to get each field
        return row[0], row[1], row[2], row[3], row[4], row[5], row[6]

    def get_item_score(self):
        cur = self.connection.cursor()

        sql = "SELECT weapon_level + helmet_level + chest_level + boots_level FROM Battles WHERE fighter_id = ?"
        cur.execute(sql, (self.id,))
        row = cur.fetchone()
        return row[0]

    def get_ticket_status(self):
        cur = self.connection.cursor()

        sql = "SELECT ticket_active FROM Lottery WHERE ticket_id = ?"
        cur.execute(sql, (self.id,))
        row = cur.fetchone()
        return row[0]

    # pass in the winning_number as a parameter from the daily script: daily_maintenance.py
    def get_lottery_winners(self, winning_number):
        cur = self.connection.cursor()
        # find ticket id's with the winning number as their ticket guess, and their active_ticket is 1, which defines a basic ticket
        sql = "SELECT ticket_id FROM Lottery WHERE ticket_guess = ? AND ticket_active = ?"
        cur.execute(sql, (winning_number, 1))
        rows = cur.fetchall()
        std_winners = []
        for row in rows:
            std_winners.append(row[0])

        # find ticket id's with the winning number as their ticket guess, and their active_ticket is 2, which defined a premium ticket
        sql = "SELECT ticket_id FROM Lottery WHERE ticket_guess = ? AND ticket_active = ?"
        cur.execute(sql, (winning_number, 2))
        rows = cur.fetchall()
        prem_winners = []
        for row in rows:
            prem_winners.append(row[0])


        # reset all tickets as well, since this function is only called when checking for winners
        self.reset_lottery()

        # return list of winner id's (basic and premium)
        return std_winners, prem_winners

    def get_shop_list(self):
        cur = self.connection.cursor()

        sql = "SELECT * from SHOP"
        cur.execute(sql)
        rows = cur.fetchall()
        return rows

    def get_shop_item(self, item_id):
        cur = self.connection.cursor()

        # test if the user ID exists in the datbase
        sql = "SELECT * FROM SHOP WHERE item_id = ?"
        cur.execute(sql, (item_id,))
        row = cur.fetchone()
        print(row)
        return row
        # see if a row exists in the fetch results, if not, they don't have an account

    def daily_all(self):
        cur = self.connection.cursor()
        cur2 = self.connection.cursor()

        # for every user, reward X * level
        for row in cur.execute('SELECT * FROM Users' ):
            sql = "UPDATE Users SET money = money + (500*level) WHERE user_id = ?"
            id = row[0]
            cur2.execute(sql, (id,))
        self.connection.commit()

    def update_money(self, amount):
        cur = self.connection.cursor()

        sql = "UPDATE Users SET money = money + ? WHERE user_id = ?"
        cur.execute(sql, (amount, self.id))
        cur.execute("select * from Users")
        rows = cur.fetchall()
        print("\nUsers table after cash update: \n")
        for row in rows:
            print(row)

        self.connection.commit()
        return self.get_money()

    def update_bank_balance(self, balance):
        cur = self.connection.cursor()

        sql = "UPDATE Users SET bank = bank + ? WHERE user_id = ?"
        cur.execute(sql, (balance, self.id))
        cur.execute("select * from Users")
        rows = cur.fetchall()
        print("\nUsers table after bank update: \n")
        for row in rows:
            print(row)

        self.connection.commit()
        return self.get_bank_balance()

    def update_level(self):
        cur = self.connection.cursor()

        sql = "UPDATE Users SET level = level + 1 WHERE user_id = ?"
        cur.execute(sql, (self.id,))
        cur.execute("select * from Users")
        rows = cur.fetchall()
        print("\nUsers table after level update: \n")
        for row in rows:
            print(row)

        self.connection.commit()
        return self.get_level()

    def update_battle_weapon(self, weapon_level):
        cur = self.connection.cursor()

        sql = "UPDATE Battles SET weapon_level = ? WHERE fighter_id = ?"
        cur.execute(sql, (weapon_level, self.id))
        cur.execute("SELECT * from Battles")
        rows = cur.fetchall()
        print("\nBattles table after battle gear update: \n")
        for row in rows:
            print(row)

        self.connection.commit()
        return self.get_item_score()

    def update_battle_helmet(self, helmet_level):
        cur = self.connection.cursor()

        sql = "UPDATE Battles SET helmet_level = ? WHERE fighter_id = ?"
        cur.execute(sql, (helmet_level, self.id))
        cur.execute("SELECT * from Battles")
        rows = cur.fetchall()
        print("\nBattles table after battle gear update: \n")
        for row in rows:
            print(row)

        self.connection.commit()
        return self.get_item_score()

    def update_battle_chest(self, chest_level):
        cur = self.connection.cursor()

        sql = "UPDATE Battles SET chest_level = ? WHERE fighter_id = ?"
        cur.execute(sql, (chest_level, self.id))
        cur.execute("SELECT * from Battles")
        rows = cur.fetchall()
        print("\nBattles table after battle gear update: \n")
        for row in rows:
            print(row)

        self.connection.commit()
        return self.get_item_score()

    def update_battle_boots(self, boots_level):
        cur = self.connection.cursor()

        sql = "UPDATE Battles SET boots_level = ? WHERE fighter_id = ?"
        cur.execute(sql, (boots_level, self.id))
        cur.execute("SELECT * from Battles")
        rows = cur.fetchall()
        print("\nBattles table after battle gear update: \n")
        for row in rows:
            print(row)

        self.connection.commit()
        return self.get_item_score()

    def update_battle_records(self, battles_lost, battles_won, total_winnings):
        cur = self.connection.cursor()

        sql = "UPDATE Battles SET battles_lost = battles_lost + ?, battles_won = battles_won + ?," \
              " total_winnings = total_winnings + ? WHERE fighter_id = ?"
        cur.execute(sql, (battles_lost, battles_won, total_winnings, self.id))
        cur.execute("select * from Battles")
        rows = cur.fetchall()
        print("\nBattles table after battle records update: \n")
        for row in rows:
            print(row)

        self.connection.commit()
        return self.get_battle_stats()

    def update_lottery_guess(self, ticket_guess, ticket_active):
        cur = self.connection.cursor()

        # update specific user's ticket guess
        # change their ticket to active in order to be considered during next drawing
        sql = "UPDATE Lottery SET ticket_guess = ?, ticket_active = ? WHERE ticket_id = ?"
        cur.execute(sql, (ticket_guess, ticket_active, self.id))
        cur.execute("SELECT * from Lottery")

        rows = cur.fetchall()
        print("\nLottery table after lottery update: \n")
        for row in rows:
            print(row)

        self.connection.commit()

    def reset_lottery(self):
        cur = self.connection.cursor()
        # set all to inactive, and change all ticket guesses to outside of our defined bounds
        sql = "UPDATE Lottery SET ticket_guess = 99999999, ticket_active = 0"
        cur.execute(sql)
        self.connection.commit()


    def reset_shop(self):
        cur = self.connection.cursor()
        sql = "DELETE FROM SHOP"
        cur.execute(sql)

        sql = "UPDATE sqlite_sequence SET seq = 0"
        cur.execute(sql)
        self.connection.commit()
