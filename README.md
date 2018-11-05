# Automated-DIBS
## About
Dibs.py is a script to reserve study rooms on campus at Tennessee Tech.

## Requirements
- Python 3.6+
- Requests module
- .ini config file with user data in _"tokens/"_

## Usage
### Linux/macOS
```console
foo@bar:~$ ./Dibs.py 
```
### Windows
```console
C:\Users\jsmith> python Dibs.py
```

# Discord-Bot
## About
A discord bot, written in python, with several utility/meme generators/RPG elements and a feature-rich hangman game.

## Run requirements:
1. Needs python 3.6+ with sqlite3, pillow, requests, and discord packages installed (use python3 -m pip install X)
2. Tokens for the discord bot login (config.txt) and IMGFLIP account password (config2.txt) must be in folder named 'tokens' in main directory. These should be 1 line text files.

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

### SQL statements used for creating the database tables:

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
