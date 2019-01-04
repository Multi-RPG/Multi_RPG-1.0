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

        # new user will start off with level 1, and $50
        sql = "INSERT INTO Users(user_id, level, money) VALUES(?, ?, ?)"
        cur.execute(sql, (self.id, 1, 50))

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

    def get_level(self):
        cur = self.connection.cursor()

        sql = "SELECT level FROM Users WHERE user_id = ?"
        cur.execute(sql, (self.id,))
        row = cur.fetchone()
        return row[0]

    def get_battle_records(self):
        cur = self.connection.cursor()

        sql = "SELECT battles_lost, battles_won, total_winnings FROM Battles WHERE fighter_id = ?"
        cur.execute(sql, (self.id,))
        row = cur.fetchone()
        # fetchone() returns only 1 row, and not in tuple format like fetchall()
        # now we can just use array indexes to get each field
        return row[0], row[1], row[2]
        
        
    def get_ticket_status(self):
        cur = self.connection.cursor()
        
        sql = "SELECT ticket_active FROM Lottery WHERE ticket_id = ?"
        cur.execute(sql, (self.id,))
        row = cur.fetchone()
        return row[0]
     

    # pass in the winning_number as a parameter from the daily script: a_lottery_script.py
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
        # set all to inactive, and change all ticket guesses to outside of our defined bounds
        sql = "UPDATE Lottery SET ticket_guess = 99999999, ticket_active = 0"
        cur.execute(sql)
        self.connection.commit()

        # return list of winner id's (basic and premium)
        return std_winners, prem_winners

    
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

    def update_battle_records(self, battles_lost, battles_won, total_winnings):
        cur = self.connection.cursor()

        sql = "UPDATE Battles SET battles_lost = battles_lost + ?, battles_won = battles_won + ?," \
              " total_winnings = total_winnings + ? WHERE fighter_id = ?"
        cur.execute(sql, (battles_lost, battles_won, total_winnings, self.id))
        cur.execute("select * from Battles")
        rows = cur.fetchall()
        print("\nBattles table after battles update: \n")
        for row in rows:
            print(row)

        self.connection.commit()
        return self.get_battle_records()

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
        return

