import sqlite3
from sqlite3 import IntegrityError
import os 

def create_database():
    conn = sqlite3.connect("links.db")  # Connect to or create the database file
    c = conn.cursor()

    # Create a table to store the links
    c.execute('''CREATE TABLE IF NOT EXISTS links
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT)''')

    conn.commit()
    conn.close()

def clear_files():
    print("Removing files: ")
    fps = os.listdir("./files")
    print(fps)
    print("You sure? Y to go. anything else to Abort.")
    c = input("> ")
    if c == "Y": 
        for f in fps: 
            os.remove("./files/"+f)
            print("deleted: %s" % f)
    else: 
        return True


