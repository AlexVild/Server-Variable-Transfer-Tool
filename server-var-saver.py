import os
import sqlite3
import sys
from shutil import copyfile

dev_db = './dev/gamedata.db'
prod_db = './prod/gamedata.db'
updated_db = './updated/gamedata.db'

### Check for proper file existence
# Remove old 'updated' DB file if there was one
if os.path.isfile(updated_db):
    os.remove(updated_db)
    print('Found existing updated file. Removed.')

if not os.path.isfile(dev_db):
    input('No gamedata.db found in ./dev. Aborting.')
    exit()

if not os.path.isfile(prod_db):
    input('No gamedata.db found in ./prod. Aborting.')
    exit()


### Connect to DBs and create cursors
prod_con = sqlite3.connect(prod_db)

copyfile(dev_db, updated_db)
if not os.path.isfile('./updated/gamedata.db'):
    input('Failed to copy new db to /updated. Aborted')
    exit()

update_con = sqlite3.connect('./updated/gamedata.db')

prod_cursor = prod_con.cursor()
update_cursor = update_con.cursor()

# At this point, we have a clone of the DEV database, with all the gamedata
# expected from any recent development. Now, let's replace any SHARED ServerVariables
# between locaitons and replace the values on this copy with those in prod

### Perform DB manipulation

change_count = 0
update_cursor.execute('SELECT Id, Name, Value FROM ServerVariables')
for row in update_cursor.fetchall():
    id = row[0]
    name = row[1]
    dev_val = row[2]
    
    # Now, check prod for its matching server variable
    prod_cursor.execute('SELECT Value FROM ServerVariables WHERE Id = ?', [id])
    prod_val = ''
    for prod_row in prod_cursor.fetchall():
        prod_val = prod_row[0]
        
    # If we have found a match, and it has some value, then replace the dev value
    # with the prod value
    if not (prod_val == '') and not ( prod_val == dev_val ):
        print(dev_val)
        print(prod_val)
        print('^====> Updating {} row with val {}'.format(name, prod_val))
        curs = update_con.cursor()
        curs.execute("UPDATE ServerVariables SET Value = ? WHERE Name = ?", [prod_val, name])
        change_count = change_count + 1

if (change_count == 0):
    input('No changes necessary. Aborting...')
    exit()

consent = input("Would you like to commit these changes to ./updated/gamedata.db? [Y/n]")

if (not (consent.lower() == 'y')):
    print("DRY RUN. No queries were committed.")
    if os.path.isfile(updated_db):
        os.remove(updated_db)
        input('Deleting temporary file in ./updated/gamedata.db')
else:
    print("COMMITTING CHANGES...")
    update_con.commit()
    update_con.close()
    prod_con.close()
    input("Done! Your new gamedata file is in ./updated/gamedata.db. Press any key to exit...")