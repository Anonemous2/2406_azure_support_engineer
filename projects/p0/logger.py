import sqlite3

# Project 0 modules:
import options

""" The logger module is responsible for choosing when to print to console,
    save command output to file, and read/update logs.
"""

# We use a SQLite DB to make logs persist, and to retrieve structured info
# later easier.
connect = sqlite3.connect('sre.db')
cursor = connect.cursor()
session_id = -1

# Session log, so we can see which actions were taken during a particular
# session.
cursor.execute("""CREATE TABLE IF NOT EXISTS session_logs (
               id INTEGER PRIMARY KEY,
               time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
               );""")

# Command log, so we can see which azure/bash commands where run, and
# during which run of the program!
cursor.execute("""CREATE TABLE IF NOT EXISTS command_logs (
               id INTEGER PRIMARY KEY,
               run_id,
               cmd VARCHAR(400),
               time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
               );""")

# Records system performance accross runs.
cursor.execute("""CREATE TABLE IF NOT EXISTS performance_logs (
               id INTEGER PRIMARY KEY,
               run_id,
               cmd VARCHAR(400),
               time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
               );""")

# Records the VMs and Azure resources created during runs, and saves the
# commands needed to delete/cleanup resources later.
cursor.execute("""CREATE TABLE IF NOT EXISTS vm_resources (
               id INTEGER PRIMARY KEY,
               run_id,
               cmd VARCHAR(400),
               time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
               );""")

def start_session():
    cursor.execute(f"INSERT INTO session_logs " \
                   f"(id) VALUES" \
                   f"(NULL)")
    session_id = cursor.lastrowid
    print(f"Session ID: {session_id}")

    
    cursor.execute(f"SELECT * FROM session_logs")
    print(f"Sessions: {cursor.fetchall()}")

    connect.commit()

def insert_performance():
    cursor.execute(f"INSERT INTO performance_logs " \
                   f"(TODO, TODO, TODO) VALUES" \
                   f"({0}, {0}, {0})")

def insert_command():
    pass

def insert_vm_resource():
    pass

def log():
    pass