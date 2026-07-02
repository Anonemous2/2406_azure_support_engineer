import re

# Tool options, which will modify the behavior of the program.
class Tools_Options():

    # Special characters for formating printed strings.
    f_error = '\033[91m'
    f_warn  = '\033[93m'
    f_bold  = '\033[1m'
    f_uline = '\033[4m'
    f_end   = '\033[0m'

    def __init__(self):
        # Script/Tool options:
        
        # TODO: Consider creating an options tuple for each option, that
        # would combine the short/long commands needed to use them, and thier
        # help info. Then use a set to store selected options for more 
        # maintainable and readable code.

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
        # TODO: Commands to view, filter, and operate on the logs.
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
    
    def help(self, cmd):
        print("Runs SRE diagnostics and can deploy VMs to azure.")
        print("")
        print(self.f_bold + self.f_uline + "Usage:" + self.f_end + \
              f" {cmd} + [OPTION]...")
        print("")
        # print(self.f_bold + self.f_uline + "Arguments:" + self.f_end + \
        #       f" {cmd} + [TODO]...")
        # print("")

        def help_format_option(short, long, info):
            c0_width = 4
            c1_width = 42
            # Format the short option in column 0.
            c0 = ' ' * c0_width
            if short:
                c0 = c0[:c0_width - 2] + \
                    f"-{self.f_bold}{short[0]}{self.f_end}"
            # Choose correct separation.
            if short and long:
                c0 += ", "
            else:
                c0 += "  "
            # Format long option in column 1.
            c1 = ' ' * c1_width
            if long:
                c1 = f"--{self.f_bold}{long}{self.f_end}" + c1[len(long) + 2:]
            print(c0 + c1 + info)
        
        print(self.f_bold + self.f_uline + "Options:" + self.f_end)
        help_format_option('n', 'nolog', 
                           'Skips writing infomation to the persistant DB.')
        help_format_option('d', 'diagnostics', 
                           'Only runs diagnostics, without creating any Azure resources.')
        help_format_option('t', 'test', 
                           'Creates a test VM that will run a HTTP server and validates functionality.')
        help_format_option('f', 'fast', 
                           'Autofills all user input, allow for easy testing.')
        help_format_option('v', 'verbose', 
                           'Prints and logs additional infomation.')
        exit(0)

    def invalid_arg(self, cmd, arg):
        print(self.f_error + "error" + self.f_end + \
              ": unexpected argument '" + \
              self.f_warn + arg + self.f_end + \
              "' found")
        print("")
        print(f"Usage: {cmd} [OPTION]...")
        print("")
        print("For more information, try '--help'.")
        # Exit with command line/syntax error.
        exit(2)
    
    # Reads a list of arguments, and activates all the options found.
    def update_from_args(self, cmd, args):
        for arg in args:
            # Using regular expressions, pull out any options.
            matches = re.search(r'^--(\w+)', arg)
            if matches:
                # Check what argument was provided.
                arg_given = matches.group(1)
                if re.search(r'^help$', arg_given, flags=re.IGNORECASE):
                    self.help(cmd)

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
                    self.invalid_arg(cmd, f"--{arg_given}")
            else:
                matches = re.search(r'^-(\w+)', arg, flags=re.IGNORECASE)
                if matches:
                    # Check what arguments were provided.
                    arg_given = matches.group(1)
                    if re.search(r'h', arg_given, flags=re.IGNORECASE):
                        self.help(cmd)

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
                        self.invalid_arg(cmd, f"-{arg_given[0]}")

# Initalize the tool-options, which will be modified by the main function logic.
active = Tools_Options()