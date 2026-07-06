import sqlite3
import subprocess
import json
import re
import sys

# Project 0 modules:
import options

""" The logger module is responsible for choosing when to print to console,
    save command output to file, and read/update logs.
"""
def run_command(cmd_list, print_output=True):
    # Wraps running a command in a try/except block, which will allow us to
    # respond to errors, print out the output.
    print(f"\nRunning command: {' '.join(cmd_list)}")
    try:
        result = subprocess.run(cmd_list, check=True, text=True, capture_output=True)
        if result.stdout and print_output:
            print(result.stdout)
        # Save cmd to the command list as a success.
        logs.insert_command(' '.join(cmd_list), False)
        return result
    # If there is an error with the command, print out the issues and return
    # 'None' which can signal the program to try a different command.
    except subprocess.CalledProcessError as e:
        print(f"\n{options.f_error}Error{options.f_end}" \
              f": Command failed with return code '{e.returncode}'", file=sys.stderr)
        print(f"Details: {e.stderr}", file=sys.stderr)
        # Save cmd to the command list as an error.
        logs.insert_command(' '.join(cmd_list), True)
        return None
    except Exception as e:
        print(f"\n{options.f_error}Error{options.f_end}" \
              f": {e}")
        # Save cmd to the command list as an error.
        logs.insert_command(' '.join(cmd_list), True)
        return None
    
class DB_Logs():

    def __init__(self):
        # We use a SQLite DB to make logs persist, and to retrieve structured info
        # later easier.
        self.connect    = sqlite3.connect('sre.db')
        self.cursor     = self.connect.cursor()
        self.session_id = -1

        # Session log, so we can see which actions were taken during a particular
        # session.
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS session_logs (
                    id INTEGER PRIMARY KEY,
                    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
                    );""")

        # Records system performance accross runs.
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS performance_logs (
                    id_ses INTEGER,
                    cpu_usage FLOAT,
                    cpu_cores INTEGER,
                    cpu_speed FLOAT,
                    mem_free VARCHAR(10),
                    mem_total VARCHAR(10),
                    store_free VARCHAR(10),
                    store_total VARCHAR(10),
                    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
                    );""")

        # Command log, so we can see which azure/bash commands where run, and
        # during which run of the program!
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS command_logs (
                    id_ses INTEGER,
                    cmd VARCHAR(400),
                    error BOOLEAN,
                    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
                    );""")

        # Records the VMs and Azure resources created during runs, and saves the
        # commands needed to delete/cleanup resources later.
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS vm_resources (
                    id_ses INTEGER,
                    name VARCHAR(50),
                    cleanup_cmd VARCHAR(400),
                    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
                    );""")
        
        # Create a new session log for this run of the tools program.
        self.cursor.execute(f"INSERT INTO session_logs " \
                            f"(id) VALUES (NULL)")
        self.session_id = self.cursor.lastrowid
        self.connect.commit()

    def print_sessions(self):
        # print(f"Session ID: {self.session_id}")
        self.cursor.execute(f"SELECT * FROM session_logs ORDER BY time ASC") 
        print_format = "{:<4} {:<20}"
        print(f"Sessions:")
        print(print_format.format('ID,', 'Timestamp'))
        for row in self.cursor.fetchall():
            print(print_format.format(*row))

    def insert_performance(self, cpu_usage, cpu_cores, cpu_speed, mem_free, mem_total, store_free, store_total):
        self.cursor.execute(f"INSERT INTO performance_logs " \
                            f"(id_ses, cpu_usage, cpu_cores, cpu_speed, " \
                            f"mem_free, mem_total, store_free, store_total) VALUES" \
                            f"('{self.session_id}', '{cpu_usage}', '{cpu_cores}', '{cpu_speed}'," \
                            f"'{mem_free}', '{mem_total}', '{store_free}', '{store_total}')")
        self.connect.commit()

    def print_performances(self):
        self.cursor.execute(f"SELECT * FROM performance_logs ORDER BY time ASC")
        print_format = "{:<4} {:<6} {:<6} {:<10} {:<10} {:<10} {:<10} {:<10} {:<20}"
        print(f"Performances:")
        print(print_format.format('ID,', '%CPU,', 'Cores,', 'Freq GHz,', 'Mem Free,', 'Mem Used,', 'Stor Free,', 'Stor Used,', 'Timestamp'))
        for row in self.cursor.fetchall():
            print(print_format.format(*row))

    def insert_command(self, command, error):
        command = command.replace("'", "''")
        self.cursor.execute(f"INSERT INTO command_logs " \
                            f"(id_ses, cmd, error) VALUES" \
                            f"('{self.session_id}', '{command}', '{error}')")
        self.connect.commit()
    
    def print_commands(self, only_errors=False):
        if only_errors:
            self.cursor.execute(f'SELECT * FROM command_logs WHERE error="True" ORDER BY time ASC')
        else:
            self.cursor.execute(f"SELECT * FROM command_logs ORDER BY time ASC")
        print_format = "{:<4} {:<8} {:<20}\n\t{:<400}"
        print(f"Commands:")
        print(print_format.format('ID,', 'Error,', 'Timestamp', 'Command'))
        for row in self.cursor.fetchall():
            if row[2] == "False":
                print(print_format.format(row[0], 'Success', row[3], row[1]))
            else:
                print(f"{options.f_error}" + \
                      print_format.format(row[0], 'Error', row[3], row[1]) + \
                        f"{options.f_end}")

    def insert_vm_resource(self, name, delete):
        self.cursor.execute(f"INSERT INTO vm_resources " \
                            f"(id_ses, name, cleanup_cmd) VALUES" \
                            f"('{self.session_id}', '{name}', '{delete}')")
        self.connect.commit()

    def execute_sql(self, query):
        try:
            self.cursor.execute(query) 
            print(self.cursor.fetchall())
        except Exception as e:
            print(f"\n{options.f_error}Error{options.f_end}" \
                  f": {e}")

    def cleanup_all(self):
        # Checks our vm_resources for resource groups, and runs the delete
        # commands on each.
        print(options.f_info + options.f_bold + "Cleaning up all resources:" + options.f_end)
        self.cursor.execute(f"SELECT * FROM vm_resources")
        for row in self.cursor.fetchall():
            try:
                if re.search(r'^az group delete', row[2]):
                    run_command(row[2].split(' '))
                    self.cursor.execute(f"DELETE FROM vm_resources WHERE name='{row[1]}'") 
                    self.connect.commit()
                else:
                    self.cursor.execute(f"DELETE FROM vm_resources WHERE name='{row[1]}'") 
                    self.connect.commit()
            except Exception as e:
                # TODO: Determine what kind of error occured, and then see if
                # we should remove this resource from our DB.
                print(e)
        

    def export_jsons(self):
        # TODO: Save all DB tables into json files for reading.
        
        # Save sessions.
        with open('sessions.json', 'w') as file:
            self.cursor.execute(f"SELECT * FROM session_logs ORDER BY time ASC") 
            for row in self.cursor.fetchall():
                row_dict = { 'id': row[0], 'time': row[1] }
                json.dump(row_dict, file, indent=4)

        # Save performance.
        with open('performance.json', 'w') as file:
            self.cursor.execute(f"SELECT * FROM performance_logs ORDER BY time ASC")
            for row in self.cursor.fetchall():
                row_dict = { 'id_ses': row[0], 'cpu_usage': row[1],
                             'cpu_cores': row[2], 'cpu_speed': row[3],
                             'mem_free': row[4], 'mem_total': row[5],
                             'store_free': row[6], 'store_total': row[7],
                             'time': row[8]}
                json.dump(row_dict, file, indent=4)

        # Save commands.
        with open('commands.json', 'w') as file:
            self.cursor.execute(f"SELECT * FROM command_logs ORDER BY time ASC")
            for row in self.cursor.fetchall():
                row_dict = { 'id_ses': row[0], 'cmd': row[1],
                             'error': row[2], 'time': row[3]}
                json.dump(row_dict, file, indent=4)

        # Save commands.
        with open('resources.json', 'w') as file:
            self.cursor.execute(f"SELECT * FROM vm_resources ORDER BY time ASC")
            for row in self.cursor.fetchall():
                row_dict = { 'id_ses': row[0], 'name': row[1],
                             'cleanup_cmd': row[2], 'time': row[3]}
                json.dump(row_dict, file, indent=4)

logs = DB_Logs()