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

        # new user will start off with level 1, $50, peace status disabled, and peace cooldown disabled
        sql = "INSERT INTO Users(user_id, level, money, peace, peace_cd) VALUES(?, ?, ?, ?, ?)"
        cur.execute(sql, (self.id, 1, 50, 0, 0))

        # new user will start off with 0 battles lost, 0 battles won, and 0 total winnings
        sql = "INSERT INTO Battles(fighter_id, battles_lost, battles_won, total_winnings) VALUES(?, ?, ?, ?)"
        cur.execute(sql, (self.id, 0, 0, 0))

        sql = "INSERT INTO Lottery(ticket_id, ticket_guess, ticket_active) VALUES(?, ?, ?)"
        cur.execute(sql, (self.id, 0, 0))

        # print users table to console after inserts
        cur.execute("select * from Users")
        rows = cur.fetchall()
        print("\nUsers after insert: \n")
        for row in rows:
            print(row)

        self.connection.commit()
        return self.get_money()

    def insert_pet(self, pet_name):
        cur = self.connection.cursor()

        # insert new pet into the database with the pet name provided as parameter
        # pets will start at level 1 and with 0 xp (experience points)
        # user's discord ID will serve as the pet_id
        sql = "INSERT INTO Pets(pet_id, pet_name, pet_xp, pet_level) VALUES(?, ?, ?, ?)"
        cur.execute(sql, (self.id, pet_name, 0, 1))

        # print pets table to console after inserts
        cur.execute("select * from Pets")
        rows = cur.fetchall()
        print("\nPets after insert: \n")
        for row in rows:
            print(row)

        self.connection.commit()

    def insert_server(self, server_id):
        cur = self.connection.cursor()

        # register the server id in the database, set announcements to 1 (to indicate announcements are active)
        sql = "Insert into SERVERS(server_id, announcements) VALUES(?, ?)"
        cur.execute(sql, (server_id, 1))

        # print servers table after insert
        cur.execute("select * from Servers")
        rows = cur.fetchall()
        print("\nServers after insert: \n")
        for row in rows:
            print(row)

        self.connection.commit()

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

    def find_pet(self):
        cur = self.connection.cursor()

        # test if the pet ID exists in the datbase
        sql = "SELECT * FROM Pets WHERE pet_id = ?"
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

    def find_server(self, server_id):
        cur = self.connection.cursor()

        sql = "SELECT * from SERVERS WHERE server_id = ?"
        cur.execute(sql, (server_id,))
        row = cur.fetchone()
        # see if a row exists in the fetch results, if not, the server isn't registered yet
        try:
            if row[0] == "":
                pass
            # the above if statement didn't throw error, so the server is registered
            return 1
        except:
            return 0

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

    def get_pet_name(self):
        cur = self.connection.cursor()

        sql = "SELECT pet_name FROM Pets WHERE pet_id = ?"
        cur.execute(sql, (self.id,))
        row = cur.fetchone()
        return row[0]

    def get_pet_xp(self):
        cur = self.connection.cursor()

        sql = "SELECT pet_xp FROM Pets WHERE pet_id = ?"
        cur.execute(sql, (self.id,))
        row = cur.fetchone()
        return row[0]

    def get_pet_level(self):
        cur = self.connection.cursor()

        sql = "SELECT pet_level FROM Pets WHERE pet_id = ?"
        cur.execute(sql, (self.id,))
        row = cur.fetchone()
        return row[0]

    def get_peace_status(self):
        cur = self.connection.cursor()

        sql = "SELECT peace FROM Users WHERE user_id = ?"
        cur.execute(sql, (self.id,))
        row = cur.fetchone()
        return row[0]

    def get_peace_cooldown(self):
        cur = self.connection.cursor()

        sql = "SELECT peace_cd FROM Users WHERE user_id = ?"
        cur.execute(sql, (self.id,))
        row = cur.fetchone()
        return row[0]

    def get_battle_stats(self):
        cur = self.connection.cursor()

        sql = (
            "SELECT weapon_level, helmet_level, chest_level, boots_level, "
            "battles_lost, battles_won, total_winnings FROM Battles WHERE fighter_id = ?"
        )
        cur.execute(sql, (self.id,))
        row = cur.fetchone()
        # fetchone() returns only 1 row, and not in tuple format like fetchall()
        # now we can just use array indexes to get each field
        return row[0], row[1], row[2], row[3], row[4], row[5], row[6]

    def get_ranks(self):
        cur = self.connection.cursor()
        sql = "SELECT * FROM BATTLES ORDER BY total_winnings DESC LIMIT 16"

        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            print(row)
        return rows

    def get_item_score(self):
        cur = self.connection.cursor()

        sql = "SELECT weapon_level + helmet_level + chest_level + boots_level FROM Battles WHERE fighter_id = ?"
        cur.execute(sql, (self.id,))
        row = cur.fetchone()
        return row[0]

    # pass in a server_id, and retrieve all fighters who registered for that server's tournament
    def get_server_tourney_members(self, server_id):
        cur = self.connection.cursor()

        sql = "SELECT fighter_id FROM Battles WHERE tourney_server_id = ?"
        cur.execute(sql, (server_id,))

        rows = cur.fetchall()
        server_fighters = []
        for row in rows:
            server_fighters.append(row[0])
        return server_fighters

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
        sql = (
            "SELECT ticket_id FROM Lottery WHERE ticket_guess = ? AND ticket_active = ?"
        )
        cur.execute(sql, (winning_number, 1))
        rows = cur.fetchall()
        std_winners = []
        for row in rows:
            std_winners.append(row[0])

        # find ticket id's with the winning number as their ticket guess, and their active_ticket is 2, which defined a premium ticket
        sql = (
            "SELECT ticket_id FROM Lottery WHERE ticket_guess = ? AND ticket_active = ?"
        )
        cur.execute(sql, (winning_number, 2))
        rows = cur.fetchall()
        prem_winners = []
        for row in rows:
            prem_winners.append(row[0])

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

    def get_server_announcements_status(self, server_id):
        cur = self.connection.cursor()
        sql = "SELECT announcements FROM SERVERS WHERE server_id = ?"
        cur.execute(sql, (server_id,))
        row = cur.fetchone()
        return int(row[0])

    def daily_all(self):
        cur = self.connection.cursor()
        cur2 = self.connection.cursor()

        # for every user, reward X * level
        for row in cur.execute("SELECT * FROM Users"):
            sql = "UPDATE Users SET money = money + (60*level) WHERE user_id = ?"
            id = row[0]
            cur2.execute(sql, (id,))
        self.connection.commit()

    # this function ADDS to bank account based off parameter given
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

    def update_pet_xp(self):
        cur = self.connection.cursor()

        # each feed will update the pet'x xp by 50
        sql = "UPDATE Pets SET pet_xp = pet_xp + 50 WHERE pet_id = ?"
        cur.execute(sql, (self.id,))
        cur.execute("select * from Pets")
        rows = cur.fetchall()
        print("\nPets table after XP update: \n")
        for row in rows:
            print(row)

        self.connection.commit()
        return self.get_pet_xp()

    def update_pet_level(self):
        cur = self.connection.cursor()

        # update pet level + 1
        sql = "UPDATE Pets SET pet_level = pet_level + 1 WHERE pet_id = ?"
        cur.execute(sql, (self.id,))
        # reset XP to 0
        sql = "UPDATE Pets SET pet_xp = 0 WHERE pet_id = ?"
        cur.execute(sql, (self.id,))
        cur.execute("select * from Pets")
        rows = cur.fetchall()
        print("\nPets table after level update: \n")
        for row in rows:
            print(row)

        self.connection.commit()
        return self.get_pet_level()

    # enables the peace status to "1", so users cannot =rob @target a user
    def toggle_peace_status(self):
        cur = self.connection.cursor()

        sql = "UPDATE Users SET peace = 1 - peace WHERE user_id = ?"
        cur.execute(sql, (self.id,))
        cur.execute("select * from Users")
        rows = cur.fetchall()
        print("\nUsers table after peace update: \n")
        for row in rows:
            print(row)

        self.connection.commit()
        return self.get_peace_status()

    # enables the peace cooldown to "1", so user cannot exit peace mode until reset
    def update_peace_cooldown(self):
        cur = self.connection.cursor()

        sql = "UPDATE Users SET peace_cd = 1 WHERE user_id = ?"
        cur.execute(sql, (self.id,))
        cur.execute("select * from Users")
        rows = cur.fetchall()
        print("\nUsers table after peace update: \n")
        for row in rows:
            print(row)

        self.connection.commit()
        return self.get_peace_status()

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

    def update_tourney_server_id(self, server_id):
        cur = self.connection.cursor()
        sql = "UPDATE Battles SET tourney_server_id = ? WHERE fighter_id = ?"
        cur.execute(sql, (server_id, self.id))
        cur.execute("SELECT * from Battles")
        rows = cur.fetchall()
        print("\nBattles table after battle gear update: \n")
        for row in rows:
            print(row)

        self.connection.commit()

    def update_battle_records(self, battles_lost, battles_won, total_winnings):
        cur = self.connection.cursor()

        sql = (
            "UPDATE Battles SET battles_lost = battles_lost + ?, battles_won = battles_won + ?,"
            " total_winnings = total_winnings + ? WHERE fighter_id = ?"
        )
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
        sql = (
            "UPDATE Lottery SET ticket_guess = ?, ticket_active = ? WHERE ticket_id = ?"
        )
        cur.execute(sql, (ticket_guess, ticket_active, self.id))
        cur.execute("SELECT * from Lottery")

        rows = cur.fetchall()
        print("\nLottery table after lottery update: \n")
        for row in rows:
            print(row)

        self.connection.commit()

    # flips a server's announcements binary value
    def toggle_server_announcements(self, server_id):
        cur = self.connection.cursor()

        sql = "UPDATE SERVERS SET announcements = 1 - announcements WHERE server_id = ?"
        cur.execute(sql, (server_id,))
        self.connection.commit()

        sql = "SELECT announcements FROM Servers WHERE server_id = ?"
        cur.execute(sql, (server_id,))

        row = cur.fetchone()
        if int(row[0]) == 1:
            return 1
        else:
            return 0

    # this will only be called in weekly maintenance script
    def reset_peace_cooldowns(self):
        cur = self.connection.cursor()
        # set all to inactive, and change all ticket guesses to outside of our defined bounds
        sql = "UPDATE USERS SET peace_cd = 0"
        cur.execute(sql)
        self.connection.commit()

    def reset_lottery(self):
        cur = self.connection.cursor()
        # set all to inactive, and change all ticket guesses to outside of our defined bounds
        sql = "UPDATE Lottery SET ticket_guess = 0, ticket_active = 0"
        cur.execute(sql)
        self.connection.commit()

    def reset_shop(self):
        cur = self.connection.cursor()
        sql = "DELETE FROM SHOP"
        cur.execute(sql)

        sql = "UPDATE sqlite_sequence SET seq = 0"
        cur.execute(sql)
        self.connection.commit()

    def reset_tourney(self):
        cur = self.connection.cursor()
        # set all fighter's server id's to 0, so they won't be pulled for the next tournament unless they register again
        sql = "UPDATE Battles SET tourney_server_id = 0"
        cur.execute(sql)
        self.connection.commit()
