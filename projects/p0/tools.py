import sys

# Project 0 modules:
import options
import diagnostics
import deploy

# Checks if we're running this file as the main script, and if so, check CLI
# arguments and execute the appropriate functions.
if __name__ == "__main__":

    # Update options from the passed CLI args.
    # Skip the first arg, as it's just the file name of this script.
    options.active.update_from_args(sys.argv[1:])

    print("Running SRE diagnostics and deployment tools.")
    print(options.active)
    print("---------------------------------------------")

    # Ok, run diagnostics on this machine.
    # TODO:
    diagnostics = diagnostics.Diagnostics()

    # Exit program if -d flag.
    if options.active.opt_diagnostics:
        print("Diagnostics complete, exiting program.")
        exit()

    # Try to deploy.
    # TODO:

    # Successful Exit.
    print("Deployment complete, exiting program.")