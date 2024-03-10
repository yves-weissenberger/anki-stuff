# -*- coding: utf-8 -*-

import sqlite3

import re

# Replace with the path to your Anki collection
anki_db_path = '/Users/yves/Library/Application Support/Anki2/User 1/collection.anki2'
deck_id = 1693638070386
# Connect to the Anki database
conn = sqlite3.connect(anki_db_path)
c = conn.cursor()

# Query to get all note IDs for a specific deck
c.execute('''SELECT notes.id, notes.flds
             FROM cards
             JOIN notes ON cards.nid = notes.id
             WHERE cards.did = ?''', (deck_id,))

# Fetch all matching records
records = c.fetchall()

updates = []
# Process each record to extract and print the last line of the Translation field
for note_id, record in records:
    try:
        # print(record)
        # Fields §are separated by the ASCII unit separator, so split on that
        fields = record.split('\x1f')

    
        # Assuming the Translation field is the first field
        # translation_field = fields[0]
        # Split the translation field into lines and get the last one
        # last_line = translation_field.split('\n')[-1]
        # print(translation_field)
        # print(len(fields))
        # for i,xx in enumerate(fields): print(i,xx)
        english_line = fields[1].split("\n")[-3]
        fields[8] = english_line

        updated_flds = '\x1f'.join(fields)
        # print("==============")
        # print(updated_flds)
        updates.append((updated_flds, note_id))
    except:
        print(record)

    # print(record)
# 
# Close the database connection
# Step 2: Update the other field to be "x" for each note
update_query = "UPDATE notes SET flds = ? WHERE id = ?"
c.executemany(update_query, updates)

conn.commit()
c.close()

conn.close()
