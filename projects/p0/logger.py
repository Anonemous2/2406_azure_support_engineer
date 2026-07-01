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

# Command log, so we can see which azure/bash commands where run, and
# during which run of the program!
cursor.execute("""CREATE TABLE IF NOT EXISTS command_logs (
               id SERIAL PRIMARY KEY,
               run_id,
               cmd VARCHAR(400),
               time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
               );""")

# Records system performance accross runs.
cursor.execute("""CREATE TABLE IF NOT EXISTS performance_logs (
               id SERIAL PRIMARY KEY,
               run_id,
               cmd VARCHAR(400),
               time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
               );""")

# Records the VMs and Azure resources created during runs, and saves the
# commands needed to delete/cleanup resources later.
cursor.execute("""CREATE TABLE IF NOT EXISTS vm_resources (
               id SERIAL PRIMARY KEY,
               run_id,
               cmd VARCHAR(400),
               time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
               );""")

def insert_performance():
    pass

def insert_command():
    pass

def insert_vm_resource():
    pass

def log():
    pass