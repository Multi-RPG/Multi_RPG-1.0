
# Discord-Bot
## About
A discord bot, written in python, with several utility/meme generators/RPG elements and a feature-rich hangman game.

## Run requirements:
1. Needs python 3.6+ with sqlite3, pillow, requests, discord, and numpy packages installed (use python3 -m pip install X)
2. .ini config files with Bot and ImgFlip account data in "tokens/"

## Usage:
### Linux/macOS
```console
foo@bar:~$ python3 ./Main.py 
```
### Windows
```console
C:\Users\jsmith> python Dibs.py
```

Note: In this repository, paths are currently setup to run in a windows environment. Adjustment will need to be made for running on Unix.

## SQL statements used for creating the database tables:

sqlite> CREATE TABLE Users(

...> user_id varchar(255) NOT NULL PRIMARY KEY,

...> level int,

...> money int

...> );

sqlite> CREATE TABLE Battles(

...> fighter_id varchar(255) NOT NULL PRIMARY KEY,

...> tourney_server_id varchar(255) NOT NULL DEFAULT 0,

...> weapon_level int DEFAULT 0,

...> helmet_level int DEFAULT 0,

...> chest_level int DEFAULT 0,

...> boots_level int DEFAULT 0,

...> battles_lost int,

...> battles_won int,

...> total_winnings int,

...> CONSTRAINT fk_users

...>     FOREIGN KEY (fighter_id)

...>     REFERENCES Users(user_id)

...>     ON UPDATE CASCADE

...>     ON DELETE CASCADE

...> );

sqlite> CREATE TABLE Lottery(

...> ticket_id varchar(255) NOT NULL PRIMARY KEY,
	
...> ticket_guess int,
	
...> ticket_active int,
	
...> CONSTRAINT fk_users2
	
...>	 FOREIGN KEY(ticket_id)
	    
...>	 REFERENCES Users(user_id)
	    
...>	 ON UPDATE CASCADE
	    
...>	 ON DELETE CASCADE
	    
...> );

sqlite> CREATE TABLE Shop(

...> item_id int NOT NULL PRIMARY KEY AUTOINCREMENT,

...> name text,

...> type text,

...> level int,

...> price int

);