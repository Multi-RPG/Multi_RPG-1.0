#!/usr/bin/env python3
import sqlite3
from sqlite3 import Error
 
class Db:
    def __init__(self, id):
        self.id = id

    '''
    # USERS TABLE
    sqlite> CREATE TABLE Users(
   ...> user_id varchar(255) NOT NULL PRIMARY KEY,
   ...> level int,
   ...> money int
   ...> );

    # BATTLES TABLE
    sqlite> CREATE TABLE Battles(
   ...> fighter_id varchar(255) NOT NULL PRIMARY KEY,
   ...> battles_lost int,
   ...> battles_won int,
   ...> total_winnings int,
   ...> CONSTRAINT fk_users
   ...>     FOREIGN KEY (fighter_id)
   ...>     REFERENCES Users(user_id)
   ...>     ON UPDATE CASCADE
   ...>     ON DELETE CASCADE
   ...> );
    '''

    def connect(self):
        try:
            # self.connection = sqlite3.connect('/usr/local/hangman.db')
            self.connection = sqlite3.connect('hangman.db')
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
