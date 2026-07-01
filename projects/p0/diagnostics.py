import subprocess

# Project 0 modules:
import options
import logger

class Diagnostics():

    def __init__(self):
        self.run_diagnostics()

    def run_diagnostics(self):
        self.run_usage()
        
    def run_usage(self):
        # Using free --human, we can get the total RAM and Swap memory 
        # avaliable.
        proc = subprocess.Popen(["top", "-n", "1", "-b"], 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.STDOUT)
        # Check if the command failed to run correctly.
        if proc.returncode != 0:
            Exception(f"Error running 'top': {proc.returncode}")

        # TODO: Log procs/process command output.
        output = proc.communicate()
        print(output[0].decode())

    def run_memory(self):
        # Using free --human, we can get the total RAM and Swap memory 
        # avaliable.
        proc = subprocess.Popen(["free", '-h'], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.STDOUT)
        # Check if the command failed to run correctly.
        if proc.returncode != 0:
            Exception(f"Error running 'free -h': {proc.returncode}")

        # TODO: Log procs/process command output.
        # output = proc.communicate()
        # print(output[0].decode())

    def run_disk(self):
        # TODO: See 'man ps' and look up what all should be collected on current
        # processes.
        proc = subprocess.Popen(["ps", '-A'], 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.STDOUT)
        # Check if the command failed to run correctly.
        if proc.returncode != 0:
            Exception(f"Error running 'ps -A': {proc.returncode}")

        # TODO: Log procs/process command output.
        # output = proc.communicate()
        # print(output[0].decode())
