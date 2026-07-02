import subprocess
import re

# Project 0 modules:
import options
import logger

class Diagnostics():

    def __init__(self):
        self.run_diagnostics()

    def run_diagnostics(self):
        self.run_usage()

    def run_cpu(self, usage):
        # Using free --human, we can get the total RAM and Swap memory 
        # avaliable.
        proc_info = subprocess.Popen(["cat", "/proc/cpuinfo"], 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.STDOUT)
        proc_speed = subprocess.Popen(["grep", "MHz"], 
                                stdin=proc_info.stdout, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.STDOUT)
        proc_cores = subprocess.Popen(["grep", "siblings"], 
                                stdin=proc_info.stdout, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.STDOUT)
        proc_name = subprocess.Popen(["grep", "model name"], 
                                stdin=proc_info.stdout, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.STDOUT)
        # Check if the command failed to run correctly.
        if proc_speed.returncode != 0:
            Exception(f"Error running 'top': {proc_speed.returncode}")
        output_speed = proc_speed.communicate()

        if proc_cores.returncode != 0:
            Exception(f"Error running 'top': {proc_cores.returncode}")
        output_cores = proc_cores.communicate()

        if proc_name.returncode != 0:
            Exception(f"Error running 'top': {proc_name.returncode}")
        output_name = proc_name.communicate()

        # TODO: Error handling (unexpected re failures).
        text_name = re.split(r'\n', output_name[0].decode())
        text_name = re.search(r'^model name\s+:\s+(.+)', text_name[0]).group(1)
        
        text_cores = re.split(r'\n', output_cores[0].decode())
        text_cores = re.search(r'^siblings\s+:\s+(\d+)', text_cores[0]).group(1)
        
        text_speed = re.split(r'\n', output_speed[0].decode())
        text_speed = round(float(re.search(r'^cpu MHz\s+:\s+(\S+)', text_speed[0]).group(1)) / 1000, 2)

        print(f'CPU: {text_name}')
        display_cpu = f'{usage}% CPU usage, {text_cores} logical processors at {text_speed} GHz'
        print(display_cpu)

        
    def run_usage(self):
        # Using free --human, we can get the total RAM and Swap memory 
        # avaliable.
        proc = subprocess.Popen(["top", "-n", "1", "-b"], 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.STDOUT)
        # Check if the command failed to run correctly.
        if proc.returncode != 0:
            Exception(f"Error running 'top': {proc.returncode}")
        output = proc.communicate()

        # TODO: Error handling (unexpected re failures).
        text_out = re.split(r'\n', output[0].decode())

        reg_ex = r'^top - (\S+).*, +\d user, +load average: (\S+), (\S+), (\S+)'
        line_top = re.search(reg_ex, text_out[0])

        reg_ex = r'^Tasks: +(\d+) total, +(\d+) running, +(\d+) sleeping, +(\d+) stopped, +(\d+) zombie'
        line_tasks = re.search(reg_ex, text_out[1])

        reg_ex = r'^%Cpu\(s\): +(\S+) us, +(\S+) sy, +(\S+) ni, +(\S+) id, +(\S+) wa, +(\S+) hi, +(\S+) si, +(\S+) st'
        line_cpu = re.search(reg_ex, text_out[2])

        reg_ex = r'^MiB Mem : +(\S+) total, +(\S+) free, +(\S+) used, +(\S+) buff/cache'
        line_mem = re.search(reg_ex, text_out[3])

        reg_ex = r'^MiB Swap: +(\S+) total, +(\S+) free, +(\S+) used. +(\S+) avail Mem'
        line_swap = re.search(reg_ex, text_out[4])

        # After parse and capturing all top info, reformat and give a summary.
        # Capture bonus CPU info for displaying.
        self.run_cpu(round(float(line_top.group(3)) * 100, 1))
        
        memory_used  = round((float(line_mem.group(3)) / float(line_mem.group(1)) \
                             * 100), 1)
        memory_free  = round((float(line_mem.group(2)) / 1024), 1)
        memory_total = round((float(line_mem.group(1)) / 1024), 1)

        display_memory = f'{memory_used}% Memory usage, ' \
            f'({memory_free} GiB free, {memory_total} GiB total)'
        print(display_memory)

        self.run_disk()

    def run_disk(self):
        # TODO: See 'man ps' and look up what all should be collected on current
        # processes.
        proc = subprocess.Popen(["df", '-hl', '--total'], 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.STDOUT)
        # Check if the command failed to run correctly.
        if proc.returncode != 0:
            Exception(f"Error running 'ps -A': {proc.returncode}")

        output = proc.communicate()

        # TODO: Error handling (unexpected re failures).
        text_out = re.split(r'\n', output[0].decode())

        reg_ex = r'total\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)'
        line = re.search(reg_ex, text_out[-2])

        display_line = f'{line.group(4)} Storage usage, ' \
            f'({line.group(3)} free, {line.group(1)} total)'
        print(display_line)
        # TODO: Log procs/process command output.

