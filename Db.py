#!/usr/bin/env python3
import sqlite3
from sqlite3 import Error
 
class Db:
    def __init__(self, id):
        self.id = id
        
    def connect(self):
        try:
            self.connection = sqlite3.connect('hangman.db')
            return self.connection
        except Error as e:
            print(e)
        
    def insert_acct(self, level, money):
        try:
            sql = "INSERT INTO Users(user_id, level, money) VALUES(?, ?, ?)"
            
            cur = self.connection.cursor()
            cur.execute(sql, (self.id, level, money))
            cur.execute("select * from Users")
            rows = cur.fetchall()
            print("\nUsers after insert: \n")
            for row in rows:
                print(row)
                
            self.connection.commit()
            return " Made account! Your starting money: " + self.get_money()
            
        except:
            return " You already have an account!! Your money: " + self.get_money()
     
    def find_acct(self):
           # test if the user ID exists in the datbase
            sql = "SELECT * FROM Users WHERE user_id = ?"
            cur = self.connection.cursor()
            cur.execute(sql, (self.id,))
            rows = cur.fetchall()
            # see if row 0 exists in the fetch results, if not, they don't have an account
            try:
                if rows[0] == "":
                    pass
                # the above if statement didn't throw error, so the account exists. return 1
                return 1
            except:
                return 0
                
    def delete_acct(self):
        try:
            if self.find_acct() == 0:
                return " You do not have an account to delete <a:rotatethink:490228030556340259>"
                
            sql = "DELETE FROM Users WHERE user_id = ?"
            
            cur = self.connection.cursor()
            cur.execute(sql, (self.id,))
            cur.execute("select * from Users")
            rows = cur.fetchall()
            print("\nUsers after delete: \n")
            for row in rows:
                print(row)
                
            self.connection.commit()
            return " Deleted account! "
            
        except:
            return " Failed to delete account... Please contact bot admin. <a:rotatethink:490228030556340259>"

    def update_money(self, amount):
        try:
            sql = "UPDATE Users SET money = money + ? WHERE user_id = ?"
            
            cur = self.connection.cursor()
            cur.execute(sql, (amount, self.id))
            cur.execute("select * from Users")
            rows = cur.fetchall()
            print("\nUsers table after cash update: \n")
            for row in rows:
                print(row)
                
            self.connection.commit()
            return "Your new account balance: " + self.get_money()
            
        except:
            return " Unable to update money. Please contact bot admin. "
            
    def get_money(self):
        try:
            sql = "SELECT money FROM Users WHERE user_id = ?"            
            cur = self.connection.cursor()
            cur.execute(sql, (self.id,))
            rows = cur.fetchall()
            return '**$' + ''.join(map(str, (rows[0]))) + '**' # awkward syntax to convert integer tuple into string
            
        except:
            return "**$0**. \nNo bank account! <a:rotatethink:490228030556340259>\n" \
                   "Use **%create** to start one. "

    def get_level(self):
        try:
            sql = "SELECT level FROM Users WHERE user_id = ?"
            cur = self.connection.cursor()
            cur.execute(sql, (self.id,))
            rows = cur.fetchall()
            return '**' + ''.join(map(str, (rows[0]))) + '**'  # awkward syntax to convert integer tuple into string

        except:
            return "**0**. \nNo bank account! <a:rotatethink:490228030556340259>\n" \
                   "Use **%create** to start one. "
