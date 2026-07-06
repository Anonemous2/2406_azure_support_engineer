import subprocess
import sys
import random

# Project 0 modules:
import options
import logger

class AzureDeployment():

    def __init__(self):
        self.rg_name = None
        self.location = None
        self.vm_name = None
        self.ip_address = None
        self.port = None

    def authenticate(self):
        pass

    def deploy(self):
        # Configure resources first.
        if self.rg_name is None:
            self.configure()
        
        self.deploy_rg()
        self.deploy_vm()

    def deploy_rg(self):
        # Configure resources first.
        if self.rg_name is None:
            self.configure_rg()

        print(options.f_info + options.f_bold + "Deploying RG:" + options.f_end)
            
        # After configuring the resources, we can run Azure CLI commands to
        # deploy the resource group and vm.
        cmd_out = None
        while cmd_out == None:
            # TODO: CHECK FOR EXISTING RG OF SAME NAME.
            cmd_list = ["az", "group", "create", "--name", self.rg_name, 
                        "--location", self.location, "--output", "table"]
            cmd_out = logger.run_command(cmd_list)
            if not cmd_out:
                # TODO: Ask if the user would like to reconfigure azure options
                # or quit program.
                if options.active.opt_fast:
                    # Just exit program.
                    print("Failed to create resource group, exiting program.")
                    exit(-1)
                print("Failed to create resource group, reconfiguring for retry.")
                self.configure_rg()
            else:
                # Add this new RG to our resource log.
                logger.logs.insert_vm_resource(self.rg_name, 
                                               f"az group delete --name {self.rg_name} --no-wait --yes")

        print(f"{self.rg_name} Created.")

    def deploy_vm(self):        
        # Configure resources first.
        if self.vm_name is None:
            self.configure_vm()

        print(options.f_info + options.f_bold + "Deploying VM:" + options.f_end)

        cmd_out = None
        while cmd_out == None:
            # Check for existing VM
            cmd_list = ["az", "vm", "list", "-g", self.rg_name, "--query", 
                        f"[?name=='{self.vm_name}'].name", "-o", "tsv"]
            cmd_out = logger.run_command(cmd_list)
            if not cmd_out.stdout.strip():
                print(f"{self.vm_name} DNE, creating it now.")
                cmd_list = [
                    "az", "vm", "create", 
                    "--resource-group", self.rg_name,
                    "--name", self.vm_name,
                    "--image", "Ubuntu2204",
                    "--size", "Standard_B2ats_v2",
                    "--storage-sku", "Standard_LRS",
                    "--boot-diagnostics-storage", "",
                    "--admin-username", "azureuser",
                    "--generate-ssh-keys",
                    "--location", self.location,
                    "--output", "table"
                ]
                cmd_out = logger.run_command(cmd_list)
                if not cmd_out:
                    # TODO: Ask if the user would like to reconfigure azure options
                    # or quit program.
                    print("Failed to create VM, exiting program.")
                    exit(-1)
                    if options.active.opt_fast:
                        # Just exit program.
                        print("Failed to create virtual machine, exiting program.")
                        exit(-1)
                    print("Failed to create virtual machine, reconfiguring for retry.")
                    self.configure_vm()
                else:
                    # Add this new VM to our resource log.
                    logger.logs.insert_vm_resource(self.vm_name, 
                                                   f"az vm deallocate --name {self.vm_name} --resource-group {self.rg_name} --no-wait")
            else:
                print(f"{self.vm_name} Already exists.")

        # Setup auto-shutdown feature, to limit costs.
        auto_shut_time = '2200' # 4 hours ahead of US EST.
        cmd_list = ["az", "vm", "auto-shutdown", "--resource-group", self.rg_name, 
                    "--name", self.vm_name, "--time", auto_shut_time]
        cmd_out = logger.run_command(cmd_list)
        if not cmd_out:
            # TODO: Ask if the user would like to reconfigure azure options
            # or quit program.
            print("Failed to create auto-shutdown rule.")

        # Open the port number as inbound.
        cmd_list = [
            "az", "network", "nsg", "rule", "create",
            "--resource-group", self.rg_name,
            "--nsg-name", f"{self.vm_name}NSG",
            "--name", "Allow_8081_Inbound",
            "--priority", "1010",
            "--destination-port-ranges", self.port,
            "--direction", "Inbound",
            "--access", "Allow",
            "--protocol", "Tcp",
            "--description", "Allow FastAPI web traffic on port 8081",
            "--output", "table"
        ]
        cmd_out = logger.run_command(cmd_list)
        if not cmd_out:
            # TODO: Ask if the user would like to reconfigure azure options
            # or quit program.
            print("Failed to create network rule.")
            
        # Fetch IP address of new virtual machine.
        cmd_list = [
            "az", "vm", "list-ip-addresses",
            "-g", self.rg_name,
            "-n", self.vm_name,
            "--query", "[0].virtualMachine.network.publicIpAddresses[0].ipAddress",
            "-o", "tsv"
        ]
        cmd_out = logger.run_command(cmd_list)
        if not cmd_out:
            print("Failed to find ip address of VM.")
        else:
            self.ip_address = cmd_out.stdout.strip().replace("\r", "")
            print(f"VM Address: {self.ip_address}")

        # TODO: Ask if the user would like to deploy a bootstrapping script

        print(f"{self.vm_name} Created.")


    def configure(self):
        # Get names for Azure resources.
        # Setup default names.
        self.rg_name  = f'rg-default-{random.randint(0, 99999)}'
        self.vm_name  = f'vm-default-{random.randint(0, 99999)}'
        self.location = 'canadaeast'
        self.port     = "8081"

        # Ask for user input, and rename resources if provided.
        if not options.active.opt_fast:
            print(options.f_info + options.f_bold + "Configure deployment options:" + options.f_end)
            self.rg_name    = input(f"Enter Resource Group [{self.rg_name}]: ").strip() \
                or self.rg_name
            self.vm_name    = input(f"Enter VM Name        [{self.vm_name}]: ").strip() \
                or self.vm_name
            self.location   = input(f"Enter Region         [{self.location}]: ").strip() \
                or self.location
            self.port       = input(f"Enter Open Port      [{self.port}]: ").strip() or \
                self.port
            print("")
        else:
            print(options.f_info + options.f_bold + "Deployment options:" + options.f_end)
            print(f"Resource Group [{self.rg_name}]")
            print(f"VM Name        [{self.vm_name}]")
            print(f"Region         [{self.location}]")
            print(f"Open Port      [{self.port}]")
            print("")

    def configure_rg(self):
        # Setup default names.
        self.rg_name  = f'rg-default-{random.randint(0, 99999)}'
        self.location = 'canadaeast'

        print(options.f_info + options.f_bold + "Configure resource group options:" + options.f_end)
        self.rg_name    = input(f"Enter Resource Group [{self.rg_name}]: ").strip() \
            or self.rg_name
        self.location   = input(f"Enter Region         [{self.location}]: ").strip() \
            or self.location
        
        # If we need to reconfigure the RG, we probably should wip VM names.
        self.clear_vm()

    def clear_vm(self):
        self.vm_name = None
        self.ip_address = None
        self.port = None

    def configure_vm(self):
        # Setup default names.
        self.vm_name  = f'vm-default-{random.randint(0, 99999)}'
        self.port     = "8081"

        print(options.f_info + options.f_bold + "Configure virtual machine options:" + options.f_end)
        self.vm_name    = input(f"Enter VM Name        [{self.vm_name}]: ").strip() \
            or self.vm_name
        self.port       = input(f"Enter Open Port      [{self.port}]: ").strip() \
            or self.port

    def cleanup(self):
        print(options.f_info + options.f_bold + "Cleaning up RG:" + options.f_end)
        if self.rg_name == None:
            print("No current resource group to cleanup.")
            return
        # Run the delete resources command on the stuff we just created.
        cmd_list = ["az", "group", "delete", "--name", self.rg_name, 
                    "--no-wait", "--yes"]
        cmd_out = logger.run_command(cmd_list)
    
    def cleanup_vm(self):
        print(options.f_info + options.f_bold + "Cleaning up VM:" + options.f_end)
        if self.vm_name == None:
            print("No current virtual machine to cleanup.")
            return
        # Run the delete resources command on the stuff we just created.
        cmd_list = ["az", "vm", "deallocate ", "--name", self.vm_name, 
                    "--resource-group", self.rg_name, "--no-wait"]
        cmd_out = logger.run_command(cmd_list)