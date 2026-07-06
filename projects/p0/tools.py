import sys
import re

# Project 0 modules:
import options
import diagnostics
import deploy
import logger

# Checks if we're running this file as the main script, and if so, check CLI
# arguments and execute the appropriate functions.
if __name__ == "__main__":
    # Update options from the passed CLI args.
    # Skip the first arg, as it's just the file name of this script.
    options.active.update_from_args(sys.argv[0], sys.argv[1:])

    # Print startup.
    print(options.f_info + options.f_bold + \
          "Running SRE diagnostics and deployment tools." + options.f_end)
    print(options.active)

    # Ok, run diagnostics on this machine.
    # Always record performance, but print based on launch options.
    performs = diagnostics.Diagnostics()
    deployment = deploy.AzureDeployment()
    
    # Check for interactive mode, and if not in it, run the default VM 
    # deployment commands.
    if not options.active.opt_interactive:
        # log and print diagnostics.
        performs.print_diagnostics()
        
        # Check for only diagnostics.
        if not options.active.opt_diagnostics:
            # Try to deploy.
            deployment.configure()
            deployment.deploy()

            print("Deployment complete, exiting program.")
            exit(0)
        else:
            print("Exiting program.")
            exit(0)
    
    # Else, we're in interactive mode, where we'll run in a loop asking the
    # user to select an option and run some functions.
    interactive_menu = {
        'performance':              "Checks and logs system's performance.",
        'deploy':                   "Creates a new resource group and virtual machine.",
        'deploy rg':                "Creates a new resouce group.",
        'configure rg':             "Select a resouce group For deploying VMs",
        'deploy vm':                "Creates a new virtual machine.",
        'cleanup':                  "Deletes all resources created by the last resource group.",
        'cleanup vm':                  "Deallocate the last vm created by the last resource group.",
        'cleanup all':              "Deletes all resources created with this program.",
        'print sessions':           "Prints out all logged sessions.",
        'print performance':        "Prints out all logged performace metrics.",
        'print commands':           "Prints out all logged commands.",
        'print errors':             "Prints out all logged failed commands.",
        'query "[SQL Query]"':      "Prints the output of running the passed query statement.",
        'export json':              "Exports all logs to json files.",
        'exit':                     "Exits the program."
    }
    def print_menu():
        print(options.f_bold + options.f_info + "Options:" + options.f_end)
        for option, info in interactive_menu.items():
            print("{:<20} {:<80}".format(option, info))
    print_menu()

    # Run in a loop until exit command.
    while True:
        cmd = input("Enter command to run: ")
        # Any input?
        if not cmd:
            continue
        cmd = cmd.lower()
        # Check for matches to run correct command.
        if re.search(r'^performance', cmd):
            performs.run_diagnostics()
            performs.print_diagnostics()
            continue
        elif re.search(r'^deploy rg', cmd):
            deployment.configure_rg()
            deployment.deploy_rg()
        elif re.search(r'^configure rg', cmd):
            deployment.configure_rg()
        elif re.search(r'^deploy vm', cmd):
            deployment.configure_vm()
            deployment.deploy_vm()
        elif re.search(r'^deploy', cmd):
            deployment.deploy()
        elif re.search(r'^cleanup all', cmd):
            logger.logs.cleanup_all()
        elif re.search(r'^cleanup vm', cmd):
            deployment.cleanup_vm()
        elif re.search(r'^cleanup', cmd):
            deployment.cleanup()
        elif re.search(r'^print sessions', cmd):
            logger.logs.print_sessions()
        elif re.search(r'^print performance', cmd):
            logger.logs.print_performances()
        elif re.search(r'^print commands', cmd):
            logger.logs.print_commands()
        elif re.search(r'^print errors', cmd):
            logger.logs.print_commands(True)
        elif re.search(r'^query "(.+)"$', cmd):
            result = re.search(r'^query "(.+)"$', cmd)
            logger.logs.execute_sql(result.group(1))
        elif re.search(r'^export json', cmd):
            logger.logs.export_jsons()
        elif re.search(r'^exit', cmd):
            print("Exiting program.")
            exit(0)
        else:
            print(options.f_error + "Error" + options.f_end + \
              ": unknown command '" + options.f_warn + cmd + options.f_end + "'")
            print_menu()