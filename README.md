
# Discord-Bot
## About
A discord bot, written in python, with several utility/meme generators/RPG elements and a feature-rich hangman game.

## Run requirements:
1. Needs python 3.6+ with sqlite3, pillow, requests, discord (0.16.12), numpy, dblpy (info on discordbots.org), and profanityfilter packages installed (use python3 -m pip install X)
2. Optional: (Recommended) Create virtual environment, run `pip install requirements.txt`;
3. In `scripts/setup/` folder, run `python setup.py`
4. In new `tokens` folder, replace value in `tokenbot.ini` with your discord bot token
 
Optional entries in `tokens` folder:
 - imgflip account token in `tokenimgflip.ini` (if meme generation desired)
 - discordbots.org token in `token_dbo_api.ini` (if uploading statistics about your bot is desired)
 - google cloud service account, save as `creds.json` to upload database backups when `backup_script.py` is run

## Usage:
### Linux/macOS
```console
foo@bar:~$ python3 ./Main.py 
```
### Windows
```console
C:\Users\jsmith> python Main.py
```

Note: In this repository, paths are currently setup to run in a windows environment. Adjustment will need to be made for running on Unix.