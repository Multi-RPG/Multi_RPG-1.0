# Discord-Bot
A discord bot, written in python, with several utility/meme generators/RPG elements and a feature-rich hangman game.

Run requirements:
1. Use python3 Main.py (or just python Main.py, but make sure python version is 3.6+ and not 2.7)
2. Needs sqlite3, pillow, requests, and discord packages installed (use python3 -m pip install X)
3. Tokens for the discord bot login (config.txt) and IMGFLIP account password (config2.txt) must be in folder named 'tokens' in main directory. These should be 1 line text files.

Note: Paths are currently setup to run in a windows environment. Adjustment will need to be made for running on Unix.

SQL statements used for creating the database tables:
-

sqlite> CREATE TABLE Users(

...> user_id varchar(255) NOT NULL PRIMARY KEY,

...> level int,

...> money int

...> );

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
