import re

# Tool options, which will modify the behavior of the program.
class Tools_Options():
    def __init__(self):
        # Script/Tool options:
        # '--help' / '-h' The script will print to console how to use tools.py,
        # and explain all launch options.
        self.opt_help = False
        # '--nolog' / '-n' Skips writing infomation to the persistant DB.
        self.opt_nolog = False
        # '--diagnostics' / '-d' Only runs diagnostics, without creating any 
        # Azure resources.
        self.opt_diagnostics = False
        # '--test' / '-t' Creates a test VM that will run a HTTP server and 
        # validates functionality.
        self.opt_test = False
        # '--fast' / '-f' Autofills all user input, allow for easy testing.
        self.opt_fast = False
        # '--verbose' / '-v' Prints and logs additional infomation.
        self.opt_verbose = False
        # TODO: More as needed.

    # Returns a nice string for functions like print.
    def __str__(self):
        active = []
        if self.opt_help:
            active.append("--help")
        if self.opt_nolog:
            active.append("--nolog")
        if self.opt_diagnostics:
            active.append("--diagnostics")
        if self.opt_test:
            active.append("--test")
        if self.opt_fast:
            active.append("--fast")
        if self.opt_verbose:
            active.append("--verbose")
        return "Active options: " + str(active)
    
    # Reads a list of arguments, and activates all the options found.
    def update_from_args(self, args):
        for arg in args:
            # Using regular expressions, pull out any options.
            matches = re.search(r'^--(\w+)', arg)
            if matches:
                # Check what argument was provided.
                arg_given = matches.group(1)
                if re.search(r'^help$', arg_given, flags=re.IGNORECASE):
                    # TODO: Print info.
                    print("TODO: HELP INFO")
                    exit()

                elif re.search(r'^nolog$', arg_given, flags=re.IGNORECASE):
                    self.opt_nolog = True

                elif re.search(r'^diagnostics$', arg_given, flags=re.IGNORECASE):
                    self.opt_diagnostics = True

                elif re.search(r'^test$', arg_given, flags=re.IGNORECASE):
                    self.opt_test = True

                elif re.search(r'^fast$', arg_given, flags=re.IGNORECASE):
                    self.opt_fast = True

                elif re.search(r'^verbose$', arg_given, flags=re.IGNORECASE):
                    self.opt_verbose = True

                else:
                    # TODO: Invalid arg info.
                    print(f"UNKNOWN ARG: --{arg_given}")
            else:
                matches = re.search(r'^-(\w+)', arg, flags=re.IGNORECASE)
                if matches:
                    # Check what arguments were provided.
                    arg_given = matches.group(1)
                    if re.search(r'h', arg_given, flags=re.IGNORECASE):
                        # TODO: Print info.
                        print("TODO: HELP INFO")
                        exit()

                    if re.search(r'n', arg_given, flags=re.IGNORECASE):
                        self.opt_nolog = True
                        arg_given = re.sub(r'n', '', arg_given, flags=re.IGNORECASE)

                    if re.search(r'd', arg_given, flags=re.IGNORECASE):
                        self.opt_diagnostics = True
                        arg_given = re.sub(r'd', '', arg_given, flags=re.IGNORECASE)

                    if re.search(r't', arg_given, flags=re.IGNORECASE):
                        self.opt_test = True
                        arg_given = re.sub(r't', '', arg_given, flags=re.IGNORECASE)

                    if re.search(r'f', arg_given, flags=re.IGNORECASE):
                        self.opt_fast = True
                        arg_given = re.sub(r'f', '', arg_given, flags=re.IGNORECASE)

                    if re.search(r'v', arg_given, flags=re.IGNORECASE):
                        self.opt_verbose = True
                        arg_given = re.sub(r'v', '', arg_given, flags=re.IGNORECASE)

                    if not re.search(r'^$', arg_given, flags=re.IGNORECASE):
                        # TODO: Invalid args info.
                        print(f"UNKNOWN ARGS: -{arg_given}")

# Initalize the tool-options, which will be modified by the main function logic.
active = Tools_Options()