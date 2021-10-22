# Server Variable Transfer Tool

## Purpose
This tool exists for use with the Intersect Engine ([Ascension Game Dev GitHub](https://github.com/AscensionGameDev "Ascension Game Dev GitHub")).

Its purpose is to UPDATE one sqlite database with the changes that a developer will make while using the engine's editor, while RETAINING the values of the "server variables" table that may have existed in the production sqlite database.

This allows things like leaderboards, or global timers, or dungeon states to be retained when a server's gamedata.db file is updated (which you would do when you want to add new items, maps, quests, events, etc, to your production server)

## Requirements
You must have python3 installed to run the script. This script is also useless unless you already have some delineation between:
1. Your "development/dev" server - where you connect to to make changes in your editor
2. Your "production/prod" server - where your PLAYERS connect to to play your game

## How to use
1. Clone this directory
2. Place your DEV `gamedata.db` file, found in `/your-local-server/resources/gamedata.db`, into the directory of this project marked `/dev`
3. Place your PROD `gamedata.db` file, found in `/your-hosted-server/resources/gamedata.db`, into the directory of this project marked `/prod`
4. Run the `server-var-saver.py` script.
5. Navigate to this project's directory `/updated`, and copy the `gamedata.db` file there - this is your updated database!
6. **MAKE A BACKUP OF YOUR HOSTED `gamedata.db` FILE ON YOUR HOSTED MACHINE**
7. Paste the new `gamedata.db` file on your hosted machine, in `/resources/`
8. Restart your server and voila!