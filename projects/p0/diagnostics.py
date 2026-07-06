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

        # Then save usage to persistent db.
        logger.logs.insert_performance(self.cpu_usage, 
                                       self.cpu_cores, 
                                       self.cpu_speed,
                                       self.mem_free, 
                                       self.mem_total,
                                       self.store_free, 
                                       self.store_total)

    def run_cpu(self):
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
        try:
            self.cpu_name = re.search(r'^model name\s+:\s+(.+)', text_name[0]).group(1)
        except Exception as e:
            # Sometimes finding the cpu name fails, skip in those cases.
            self.cpu_name = " "
            
        text_cores = re.split(r'\n', output_cores[0].decode())
        self.cpu_cores = re.search(r'^siblings\s+:\s+(\d+)', text_cores[0]).group(1)
        
        text_speed = re.split(r'\n', output_speed[0].decode())
        self.cpu_speed = round(float(re.search(r'^cpu MHz\s+:\s+(\S+)', 
                                               text_speed[0]).group(1)) / 1000, 2)

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
        self.cpu_usage = round(float(line_top.group(3)) * 100, 1)
        self.run_cpu()
        
        self.mem_used  = round((float(line_mem.group(3)) / float(line_mem.group(1)) \
                             * 100), 1)
        self.mem_free  = round((float(line_mem.group(2)) / 1024), 1)
        self.mem_total = round((float(line_mem.group(1)) / 1024), 1)

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

        self.store_usage = line.group(4)
        self.store_free  = line.group(3)
        self.store_total = line.group(1)

    def print_diagnostics(self):
        # Use format string to get a more readable output.
        print(options.f_info + options.f_bold + "System Performace:" + options.f_end)
        print_format = " {:>4} {:<14} {:<60}"
        # CPU
        print(f' CPU: {self.cpu_name}')
        print(print_format.format(f'{self.cpu_usage}%', 'CPU usage,',
                                  f'{self.cpu_cores} logical processors at {self.cpu_speed} GHz'))
        # Memory
        print(print_format.format(f'{self.mem_used}%', 'Memory usage,',
                                  f'({self.mem_free} GiB free, {self.mem_total} GiB total)'))
        # Storage
        print(print_format.format(f'{self.store_usage}', 'Storage usage,',
                                  f'({self.store_free} free, {self.store_total} total)'))


