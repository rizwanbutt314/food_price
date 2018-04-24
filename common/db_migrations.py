import sqlite3
from sqlite3 import Error
from constants import DATABASE
import os

def create_connection():
    print("Creating datatbase...")
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
    try:
        conn = sqlite3.connect(DATABASE)
        return conn
    except Error as e:
        print(e)


def run_migrations():
    conn = create_connection()
    cur = conn.cursor()

    # Create table
    print("Creating Table...")
    cur.execute('''CREATE TABLE business
                     (  url text, business_name text,
                        rating text, cuisines text, address text,
                        p_name text, p_sub_name text, p_category text,
                        p_description text, p_price text)''')
    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
    print("Completed!")


run_migrations()
