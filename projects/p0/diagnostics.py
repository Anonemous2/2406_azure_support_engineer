""" Python file that handles the running of linux commands to gather current
    system resource utilization and logging. """

import subprocess

class Diagnostics():

    def __init__(self):
        self.run_diagnostics()

    def run_diagnostics(self):
        """ Checks the current status of this machine, logging the results to
            a log file with the current time. """
        
        # TODO: See 'man ps' and look up what all should be collected on current
        # processes.
        result = subprocess.Popen(["ps", '-A'], 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.STDOUT)
        # Check if the command failed to run correctly.
        if result.returncode != 0:
            Exception(f"SubProc returned a code of {result.returncode}")

        output = result.communicate()
        # Test output
        print(output[0].decode())

# TEMP: TODO: REMOVE
# Just create the diagnostics class.
run_diagnostics = Diagnostics()