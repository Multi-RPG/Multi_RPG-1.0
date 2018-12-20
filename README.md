
# Discord-Bot
## About
A discord bot, written in python, with several utility/meme generators/RPG elements and a feature-rich hangman game.

## Run requirements:
1. Needs python 3.6+ with sqlite3, pillow, requests, and discord packages installed (use python3 -m pip install X)
2. If using crontab for automation, file paths need to be replaced with your environment's full file paths
3. .ini config files with Bot and ImgFlip account data in "tokens/"


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

...> battles_lost int,

...> battles_won int,

...> total_winnings int,

...> CONSTRAINT fk_users

...>     FOREIGN KEY (fighter_id)

...>     REFERENCES Users(user_id)

...>     ON UPDATE CASCADE

...>     ON DELETE CASCADE

...> );


sqlite> CREATE Table Lottery(

   ...> ticket_id varchar(255) NOT NULL PRIMARY KEY,
   
   ...> ticket_guess int,
   
   ...> ticket_active int,
   
   ...> CONSTRAINT fk_users2
   
   ...> FOREIGN KEY (ticket_id)
   
   ...> REFERENCES Users(user_id)
   
   ...> ON UPDATE CASCADE
   
   ...> ON DELETE CASCADE
   
   ...> );

