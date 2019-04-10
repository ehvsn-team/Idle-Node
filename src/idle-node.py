#!/usr/bin/env python

# Import directives
try:
    import os
    import sys
    import time
    import platform
    import traceback
    
    import socket
    import requests
    
    from getpass import getpass
    
    from core import ansi
    from core import login
    from core import quote
    from core import cowsay
    from core import logger
    from core import gethost
    from core import printer
    from core import simplelib
    from core import asciigraphs
    from core import config_handler

except ImportError:
    # Prints if error is encountered while importing modules.
    print("Import Error!")
    print()
    print("==================== TRACEBACK ====================")
    traceback.print_exc()
    print("===================================================")
    sys.exit(1)
    
else:
    # Define global variables.
    STARTED = False
    
"""
FOR DEVELOPERS

Exit codes:

0 = Proper exit
1 = Force quit (Usually by CTRL+C and/or CTRL+D)
2 = Unknown command 
3 = Internet connection error
4 = Both values does not match error
5 = No module named <module>
6 = Unknown DDNS provider.
7 = Python version not supported.
10 = Unknown error occured.

"""

class MainClass(object):
    """
    MainClass():
        This is the main class of the program.
    """
    
    def __init__(self):
        """
        def __init__():
            This is the initialization method of MainClass() class.
        """

        # Define high-priority variables.
        self.logfile = 'data/logfile.log'
        self.configfile = 'data/config.dat'
        
        # Start the logger.
        self.logger = logger.LoggingObject(
                name='ArchariosFramework',
                logfile=self.logfile
                )
        
        self.logger.set_logging_level('NOTSET')
        
        self.logger.info("Running program on {0}...".format(time.asctime()))
        
        # Get the global variables.
        self.logger.info("Getting global variables...")
        global STARTED
        
        # Define program variables.
        self.logger.info("Defining program variables...")
        self.PROGRAM_NAME = "Idle-Node"
        self.PROGRAM_VERSION = "0.0.0.2"
        self.PROGRAM_DESCRIPTION = "An open-source command-line messaging platform"
        self.PROGRAM_BANNER = """\
        _ ___  _    ____    _  _ ____ ___  ____ 
        | |  \ |    |___ __ |\ | |  | |  \ |___ 
        | |__/ |___ |___    | \| |__| |__/ |___ v{1}
    {0}""".format(self.PROGRAM_DESCRIPTION, self.PROGRAM_VERSION)
    
        self.simplelib = simplelib.SimpleLib()
    
        # Check if STARTED is False.
        # If false, initialize program.
        self.logger.info("Checking if STARTED is False...")
        if STARTED is False:
            self.logger.info("STARTED is False, calling initialize() method...")
            self.initialize()
            
        else:
            self.logger.info("STARTED is True, skipping initialization...")
            
    def initialize(self):
        """
        def initialize():
            Initialize the program.
        """
        
        self.logger.info("initialize() method called by {0}().".format(sys._getframe().f_back.f_code.co_name))
        if prompt is None:
            prompt = self.PROGRAM_NAME
            
        self.logger.info("User uses {0}.".format(platform.python_implementation()))
        if platform.python_implementation() != 'CPython':
            printer.Printer().print_with_status("You are not using CPython!", 1)
            printer.Printer().print_with_status("{0} in {1} is not yet tested. YOU MAY ENCOUNTER BUGS.".format(self.PROGRAM_NAME, platform.python_implementation()), 1)
            
        pyversion = sys.version_info
        self.logger.info("User uses {0} v{1}.{2}.{3}".format(platform.python_implementation(), pyversion[0], pyversion[1], pyversion[2]))
        if pyversion[0] < 3 or pyversion[1] < 6 or pyversion[2] < 0:
            printer.Printer().print_with_status("This version of python is not supported!", 1)
            printer.Printer().print_with_status("You have `v{0}.{1}.{2}`. To run {3}, you must have CPython `v3.6.0`.".format(
                pyversion[0], pyversion[1], pyversion[2], self.PROGRAM_NAME), 1)
            
            try:
                sys.exit(7)
                
            except SystemExit:
                os._exit(7)
        
        else:
            del pyversion
        
        self.logger.info("Getting program data...")
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, "Starting {0}...".format(self.PROGRAM_NAME), "loading", 0.15)
        # Get program data.
        # Get the list of IPs.
        self.logger.info("Getting IP list...")
        self.contact_list = config_handler.ConfigHandler(self.configfile).get("ip_list")
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, "Starting {0}...".format(self.PROGRAM_NAME), "loading", 0.15)
        # Get prompts
        # Main prompt
        self.logger.info("Getting main prompt...")
        self.prompt_main = config_handler.ConfigHandler(self.configfile).get("prompt_main")
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, "Starting {0}...".format(self.PROGRAM_NAME), "loading", 0.15)
        # Prompt when using Peer-to-Peer chat.
        self.logger.info("Getting peer-to-peer prompt...")
        self.prompt_p2p_chat = config_handler.ConfigHandler(self.configfile).get("prompt_p2p_chat")
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, "Starting {0}...".format(self.PROGRAM_NAME), "loading", 0.15)
        # Prompt when using Group Chat/Conference Room.
        self.logger.info("Getting group chat/conference room prompt...")
        self.prompt_gc_chat = config_handler.ConfigHandler(self.configfile).get("prompt_gc_chat")
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, "Starting {0}...".format(self.PROGRAM_NAME), "loading", 0.15)
        # Prompt when editing config files.
        self.logger.info("Getting settings/config panel prompt...")
        self.prompt_settings_panel = config_handler.ConfigHandler(self.configfile).get("prompt_settings_panel")
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, "Starting {0}...".format(self.PROGRAM_NAME), "loading", 0.15)
        # User details.
        self.logger.info("Getting username...")
        self.username = config_handler.ConfigHandler(self.configfile).get("username")
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, "Starting {0}...".format(self.PROGRAM_NAME), "loading", 0.15)
        self.logger.info("Getting userpass...")
        self.userpass = config_handler.ConfigHandler(self.configfile).get("userpass")
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, "Starting {0}...".format(self.PROGRAM_NAME), "loading", 0.15)
        self.logger.info("Getting user IP Address...")
        try:
            self.userip = requests.get('https://api.ipify.org/').text
            
        except(socket.gaierror, requests.packages.urllib3.exceptions.NewConnectionError,
               requests.packages.urllib3.exceptions.MaxRetryError,
               requests.exceptions.ConnectionError):
            self.latest_traceback = traceback.format_exc()
            self.logger.error("An error occured while getting user's IP Address.")
            self.userip = ""
            
        else:
            self.logger.info("User's IP Address is `{0}`.".format(self.userip))
            
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, "Starting {0}...".format(self.PROGRAM_NAME), "loading", 0.15)
        self.logger.info("Setting chat placeholders...")
        self.recvname = ""
        self.recvpass = ""
        self.recvip = ""
        self.gcname = ""
        self.gcpass = ""
        self.gcip = ""
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, "Starting {0}...".format(self.PROGRAM_NAME), "loading", 0.15)
        self.logger.info("Setting latest traceback placeholder...")
        self.latest_traceback = ""
        self.latest_error_code = 0
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, "Starting {0}...".format(self.PROGRAM_NAME), "loading", 0.15)
        self.logger.info("Setting command placeholder...")
        self.command = ""
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, "Starting {0}...".format(self.PROGRAM_NAME), "loading", 0.15)
        self.logger.info("Setting main method loop...")
        self.byebye = False
        
        self.logger.info("Finished loading!")
        if prompt.endswith('.'):
            asciigraphs.ASCIIGraphs().animated_loading_screen_manual(True, "{0} Done!".format(prompt), "loading", 0.15)
            
        else:
            asciigraphs.ASCIIGraphs().animated_loading_screen_manual(True, "{0}... Done!".format(prompt), "loading", 0.15)
            
        self.logger.info("first_run value is `{0}`.".format(config_handler.ConfigHandler(self.configfile).get("first_run")))
        # print(config_handler.ConfigHandler(self.configfile).get("first_run"))  # DEV0005
        # print(type(config_handler.ConfigHandler(self.configfile).get("first_run")))  # DEV0005
        if config_handler.ConfigHandler(self.configfile).get("first_run") is True:
            if self.first_run() == 0:
                config_handler.ConfigHandler(self.configfile).set("first_run", "False")
                return 0
                
            else:
                return 1
            
        else:
            return 0
        
    def first_run(self):
        """
        def first_run():
            Run a "Wizard" to help the user set up.
        """
        
        self.logger.info("first_run() method called by {0}().".format(sys._getframe().f_back.f_code.co_name))
        try:
            print("\n===============================")
            print("Welcome to {0}!".format(self.PROGRAM_NAME))
            print("===============================")
            print()
            print("Do you want to continue using this first-run wizard? (y/n)")
            while True:
                try:
                    first_run_ask = str(input("Answer: "))
                    
                    if first_run_ask.lower() == 'y':
                        break
                    
                    elif first_run_ask.lower() == 'n':
                        printer.Printer().print_with_status("Type `first_run` in the main terminal to run this wizard.", 0)
                        return 0
                    
                except(KeyboardInterrupt, EOFError):
                    continue
                
            while True:
                try:
                    username = input("Username: ")
                    break
                    
                except(KeyboardInterrupt, EOFError):
                    continue
        
            while True:
                try:
                    userpass = getpass("Password: ")
                    checkpass = getpass("Confirm Password: ")
                    if userpass == checkpass:
                        break
                    
                    else:
                        printer.Printer().print_with_status("Both passwords does not match!", 2)
                        continue
                    
                except(KeyboardInterrupt, EOFError):
                    continue

            while True:
                try:
                    print("Do you need a DDNS?")
                    print("(DDNS is usually used if you have a dynamic IP.)")
                    printer.Printer().print_with_status("For more info, search on your favorite search engine.", 0)
                    use_ddns = input("Answer (y/n): ")
                    if use_ddns.lower() == 'y':
                        use_ddns = True
                        break
                        
                    elif use_ddns.lower() == 'n':
                        use_ddns = False
                        break
                        
                    else:
                        continue
                    
                except(KeyboardInterrupt, EOFError):
                    continue
                
            if use_ddns is True:
                print("Supported DDNS Providers:")
                print("    -DuckDNS.org        -noip.com")
                print()
                while True:
                    try:
                        ddns_provider = input("Please enter your DDNS Provider: ")
                        
                        if "duckdns" in  ddns_provider.lower():
                            ddns_provider = "DuckDNS"
                            break
                            
                        elif "noip" in  ddns_provider.lower():
                            ddns_provider = "noip"
                            break
                            
                        else:
                            continue
                        
                    except(TypeError, ValueError, EOFError, KeyboardInterrupt):
                        continue
                    
            else:
                pass
            
            if use_ddns is True:
                if ddns_provider == "DuckDNS":
                    while True:
                        try:
                            ddns_domain = input("Enter your DuckDNS.org domain name: ")
                            ddns_token = getpass("Enter your DuckDNS.org token: ")
                            break
                            
                        except(KeyboardInterrupt, EOFError):
                            continue
                        
                elif ddns_provider == "noip":
                    while True:
                        try:
                            ddns_domain = input("Enter your noip.com domain name: ")
                            ddns_username = input("Enter your noip.com username: ")
                            ddns_userpass = getpass("Enter your noip.com password: ")
                            ddns_token = ddns_username + ':::' + ddns_userpass
                            del ddns_username
                            del ddns_userpass
                            break
                            
                        except(KeyboardInterrupt, EOFError):
                            continue
                        
                else:
                    printer.Printer().print_with_status("Unknown DDNS provider!", 2)
                    return 6
                
        except(TypeError, ValueError):
            printer.Printer().print_with_status("An error occured when starting the First-run wizard.", 2)
            self.latest_traceback = traceback.format_exc()
            return 10
        
        else:
            total_items = 6
            asciigraphs.ASCIIGraphs().progress_bar_manual("Saving settings...", 0, total_items)
            config_handler.ConfigHandler(self.configfile).set("first_run", "False")
            asciigraphs.ASCIIGraphs().progress_bar_manual("Saving settings...", 1, total_items)
            config_handler.ConfigHandler(self.configfile).set("username", username)
            asciigraphs.ASCIIGraphs().progress_bar_manual("Saving settings...", 2, total_items)
            config_handler.ConfigHandler(self.configfile).set("userpass", userpass)
            asciigraphs.ASCIIGraphs().progress_bar_manual("Saving settings...", 3, total_items)
            config_handler.ConfigHandler(self.configfile).set("ddns", str(use_ddns))
            asciigraphs.ASCIIGraphs().progress_bar_manual("Saving settings...", 4, total_items)
            config_handler.ConfigHandler(self.configfile).set("ddns_provider", ddns_provider)
            asciigraphs.ASCIIGraphs().progress_bar_manual("Saving settings...", 5, total_items)
            config_handler.ConfigHandler(self.configfile).set("ddns_domain", ddns_domain)
            asciigraphs.ASCIIGraphs().progress_bar_manual("Saving settings...", 6, total_items)
            config_handler.ConfigHandler(self.configfile).set("ddns_token", ddns_token)
            self.initialize("Updating values...")
            return 0
            
    def update_ddns_service(self):
        """
        def update_ddns_service():
            Update DDNS if user uses one.
        """
        
        self.logger.info("update_ddns_service() method called by {0}().".format(sys._getframe().f_back.f_code.co_name))
        if self.use_ddns is True:
            self.logger.info("Updating DDNS Service...")
            if self.ddns_provider == "DuckDNS":
                try:
                    duckdns_recv = requests.get("https://www.duckdns.org/update?domains={0}&token={1}&ip={2}&verbose=true".format(self.ddns_domain, self.ddns_token, self.userip)).text
                    duckdns_recv = duckdns_recv.split('\n')
                    # print(duckdns_recv)  # DEV0005
                    if duckdns_recv[0] == "OK":
                        if duckdns_recv[1] == self.userip:
                            if duckdns_recv[3] == "UPDATED":
                                self.logger.info("No problems are encountered when updating DDNS.")
                                
                            else:
                                self.logger.warning("DuckDNS returns `NOCHANGE`. Record is not updated.")
                                
                        else:
                            self.logger.warning("DuckDNS record is not the same as the value in self.userip!")
                            
                    else:
                        self.logger.error("KO! KO! DuckDNS replies.")
                        
                except(socket.gaierror, requests.packages.urllib3.exceptions.NewConnectionError,
                   requests.packages.urllib3.exceptions.MaxRetryError,
                   requests.exceptions.ConnectionError):
                    self.latest_traceback = traceback.format_exc()
                    self.logger.error("An error occured while updating DDNS.")
                    
            elif self.ddns_provider == "noip":
                try:
                    no_ip_updater.update(self.ddns_token.partition(':::')[0], self.ddns_token.partition(':::')[2], self.ddns_domain, self.userip)
                    
                except BaseException as error:
                    self.latest_traceback = traceback.format_exc()
                    self.logger.error("An error occured while updating DDNS.")
                    
            elif self.ddns_provider == "None":
                pass
                    
            else:
                self.logger.error("self.ddns_provider contains an unknown value: `{0}`".format(self.ddns_provider))
                                  
        else:
            self.logger.info("User does not use DDNS service. Using IP address as the identity of user.")
        
    def substitute(self, string):
        """
        def substitute():
            Replace strings with the current value.
        """
        
        self.logger.info("substitute() method called by {0}().".format(sys._getframe().f_back.f_code.co_name))
        result = string.replace("$USERNAME", self.username).replace("$USERIP", self.userip)
        result = result.replace("$RECVNAME", self.recvname).replace("$RECVIP", self.recvip)
        result = result.replace("$GCNAME", self.gcname).replace("$GCIP", self.gcip)
        
        return result
    
    def help(self, what="main"):
        """
        def help():
            Return help string.
        """
        
        self.logger.info("help() method called by {0}().".format(sys._getframe().f_back.f_code.co_name))
        if what == "main":
            return """\
help | ?                            Show this help menu.
config | settings                   Access the Settings/Customization Panel.
update [OPTION]                     Update status of [OPTION]. (Type `update ?` for more info.)
first_run                           Start the first-run wizard.
clrscrn | cls | clr                 Clear the contents of the screen.

exit | quit | bye | shutdown        Quit {0}.""".format(self.PROGRAM_NAME)

        elif what == "config_panel":
            return """\
help | ?                    Show this help menu.
show                        List configuration values.
set [OPTION] [VALUE]        Set the value for `OPTION`.
discard [OPTION]            Discard changes made to `OPTION`.
save                        Save current settings to configuration file.
clrscrn | cls | clr         Clear the contents of the screen.

back                        Exit the Settings panel."""

        elif what == "update":
            return """\
help | ?        Show this help menu.
ip              Update YOUR IP Address.
"""

        else:
            raise ValueError("Unknown string is passed to help method.")
    
    def parse_command(self, command):
        """
        def parse_command():
            Parse the command.
        """
        
        self.logger.info("parse_command() called by {0}().".format(sys._getframe().f_back.f_code.co_name))
        if command.lower().startswith(("help", "?")):
            self.logger.info("Printing help.")
            print(self.help())
            print()
            return 0
        
        elif command.lower().startswith(("config", "settings")):
            self.logger.info("Starting config editor.")
            return self.config_editor()
        
        elif command.lower().startswith(("update",)):
            self.logger.info("Calling update method...")
            return self.update_status(command)
        
        elif command.lower().startswith(("first_run",)):
            return self.first_run()
        
        elif command.lower().startswith(("cls", "clear", "clr")):
            self.simplelib.clrscrn()

        elif command.lower().startswith(("exit", "quit", "bye", "shutdown")):
            self.byebye = True
            return 0
        
        else:
            self.logger.info("Unknown command entered.")
            printer.Printer().print_with_status("Unknown command `{0}`! Type `help` for more info.".format(command), 2)
            print()
            return 2
        
    def config_editor(self):
        """
        def config_editor():
            The Settings/Customization Panel.
        """
        
        self.logger.info("config_editor() called by {0}().".format(sys._getframe().f_back.f_code.co_name))
        self.logger.info("Getting configuration file data...")
        config_lines = config_handler.ConfigHandler(self.configfile).get()
        self.logger.info("Entering loop...")
        while True:
            try:
                config_command = str(input(self.substitute(self.prompt_settings_panel)))
                if config_command.lower().startswith(("help", "?")):
                    self.logger.info("Showing help menu.")
                    print(self.help("config_panel"))
                    print()
                    
                elif config_command.lower().startswith(("show")):
                    self.logger.info("Printing all available settings.")
                    for line in config_lines:
                        if line.startswith(("#",)):
                            continue
                        
                        elif line == "":
                            continue
                        
                        elif line.startswith("first_run="):
                            continue
                        
                        elif 'pass' in line.partition('=')[0]:
                            printer.Printer().print_with_status("{0}: {1}".format(
                                line.partition('=')[0], ('*' * len(line.partition('=')[2]))), 0)
                            
                        elif '=' in line:
                            printer.Printer().print_with_status(line.replace('=', ': '), 0)
                            # print(line.endswith("\n"))  # DEV0005: for debugging purposes only!
                            
                        else:
                            continue
                        
                    print()
                    
                elif config_command.lower().startswith(("set")):
                    self.logger.info("Set command called.")
                    config_command = config_command.split(' ')
                    try:
                        self.logger.info("Getting option and its value...")
                        option = config_command[1]
                        value = config_command[2]
                        
                    except IndexError:
                        self.logger.error("Cannot get option and value.")
                        printer.Printer().print_with_status("USAGE: set [OPTION] [VALUE]", 2)
                        continue
                    
                    if option.startswith(('#', "first_run=")):
                        self.logger.error("Invalid option supplied.")
                        printer.Printer().print_with_status("Invalid option!", 2)
                        continue
                    
                    elif option == "":
                        self.logger.error("Invalid option supplied.")
                        printer.Printer().print_with_status("Invalid option!", 2)
                        continue
                                        
                    else:
                        if 'pass' in option:
                            self.logger.info("Asking user to re-enter the value.")
                            value_verification = str(getpass("Please re-enter the value for `{0}`: ".format(option)))
                            if value_verification == value:
                                del value_verification
                            
                            else:
                                printer.Printer().print_with_status("Both values does not match!", 2)
                                continue

                        self.logger.info("Updating config lines...")
                        new_config_lines = []
                        changed = False
                        for line in config_lines:
                            # self.logger.debug("line contains `{0}`".format(line.replace('\n', '')))
                            if line.startswith(option + '='):
                                self.logger.info("line starts with `{0}=`".format(option))
                                self.logger.info("Appending new value for option.")
                                new_config_lines.append(option + '=' + value)
                                changed = True
                                
                            else:
                                self.logger.info("line does not start with `{0}=`".format(option))
                                self.logger.info("Keeping things untouched.")
                                new_config_lines.append(line)
                                
                        self.logger.info("Checking if program has changed the value...")
                        if changed is False:
                            self.logger.error("Cannot find option `{0}` in the config file!".format(option))
                            printer.Printer().print_with_status("Cannot find option `{0}`!".format(option), 2)
                            
                        else:
                            self.logger.info("Program has changed the value.")
                            self.logger.info("Transferring new lines to old variable.")
                            config_lines = new_config_lines
                            del new_config_lines
                        
                elif config_command.lower().startswith(("discard",)):
                    self.logger.info("Discard command called.")
                    config_command = config_command.split(' ')
                    try:
                        self.logger.info("Getting option to discard...")
                        option = config_command[1]
                        
                    except IndexError:
                        self.logger.error("Cannot get option and value.")
                        printer.Printer().print_with_status("USAGE: discard [OPTION]", 2)
                        continue
                    
                    if option == "*":
                        # DEV0004: All changed settings will be discarded.
                        printer.Printer().print_with_status("This feature is not yet made. Sorry!", 1)
                        continue
                    
                    else:
                        if option.startswith(('#', "first_run=")):
                            self.logger.error("Invalid option supplied.")
                            printer.Printer().print_with_status("Invalid option!", 2)
                            continue
    
                        elif option == "":
                            self.logger.error("Invalid option supplied.")
                            printer.Printer().print_with_status("Invalid option!", 2)
                            continue
                        
                        else:
                            value = config_handler.ConfigHandler(self.configfile).get(option)
                            self.logger.info("Updating config lines...")
                            new_config_lines = []
                            for line in config_lines:
                                # self.logger.debug("line contains `{0}`".format(line.replace('\n', '')))
                                if line.startswith(option + '='):
                                    self.logger.info("line starts with `{0}=`".format(option))
                                    self.logger.info("Appending new value for option.")
                                    new_config_lines.append(option + '=' + str(value))
                                    
                                else:
                                    self.logger.info("line does not start with `{0}=`".format(option))
                                    self.logger.info("Keeping things untouched.")
                                    new_config_lines.append(line)
                                    
                            self.logger.info("Checking if program has changed the value...")
                            if changed is False:
                                self.logger.error("Cannot find option `{0}` in the config file!".format(option))
                                printer.Printer().print_with_status("Cannot find option `{0}`!".format(option), 0)
                                
                            else:
                                self.logger.info("Program has changed the value.")
                                self.logger.info("Transferring new lines to old variable.")
                                config_lines = new_config_lines
                                del new_config_lines
                                
                elif config_command.lower().startswith(("save",)):
                    self.logger.info("Saving settings to configuration file...")
                    printer.Printer().print_with_status("Saving current settings to configuration file...", 0)
                    for config_line in config_lines:
                        if config_line.startswith(("#", "first_run")):
                            continue
                        
                        elif config_line == "":
                            continue
                        
                        else:
                            self.logger.info("Writing `{0}` to `{1}`...".format(config_line.partition('=')[0], self.configfile))
                            # print(config_line.partition('=')[0], '=', config_line.partition('=')[2])  # DEV0005
                            config_handler.ConfigHandler(self.configfile).set(config_line.partition('=')[0], config_line.partition('=')[2])
                            
                    printer.Printer().print_with_status("Saving current settings to configuration file... Done!", 0)
                    printer.Printer().print_with_status("Please restart {0} to use the new configuration.".format(self.PROGRAM_NAME), 1)
                    continue
                
                elif config_command.lower().startswith(("cls", "clear", "clr")):
                    self.simplelib.clrscrn()
                    
                elif config_command.lower().startswith(("back",)):
                    return 0
                    
                else:
                    self.logger.info("Unknown command entered.")
                    printer.Printer().print_with_status("Unknown command `{0}`! Type `help` for more info.".format(config_command), 2)
                    continue
                
            except(KeyboardInterrupt, EOFError):
                self.logger.warning("CTRL+C and/or CTRL+D detected, forcing to quit...")
                return 1
            
    def update_status(self, command):
        """
        def update_status():
            Update status of [OPTION].
        """
        
        self.logger.info("update_status() method called by {0}().".format(sys._getframe().f_back.f_code.co_name))
        command = command.split(' ')
        
        try:
            if command[1].startswith(("?", "help")):
                self.logger.info("Showing `update` command's help.")
                print(self.help("update"))
                return 0
            
            elif command[1].startswith(("ip",)):
                self.logger.info("Updating IP Address of user.")
                printer.Printer().print_with_status("Updating your IP Address...", 0)
                try:
                    self.userip = requests.get('https://api.ipify.org/').text
    
                except(socket.gaierror, requests.packages.urllib3.exceptions.NewConnectionError,
                       requests.packages.urllib3.exceptions.MaxRetryError,
                       requests.exceptions.ConnectionError):
                    self.latest_traceback = traceback.format_exc()
                    self.logger.error("Cannot update IP Address of user.")
                    self.userip = ""
                    printer.Printer().print_with_status("There is a problem while getting your IP Address!", 2)
                    printer.Printer().print_with_status("Do you have a stable internet connection?", 1)
                    return 3
                    
                else:
                    self.logger.info("User's IP Address is `{0}.{1}.{2}.{3}`.".format(self.userip.split('.')[0], len(str(self.userip.split('.')[1])), len(str(self.userip.split('.')[2])), self.userip.split('.')[3]))
                    printer.Printer().print_with_status("Your IP Address is: `{0}`.".format(), 0)
                    return 0
                
            else:
                self.logger.info("Unknown option/s supplied.")
                printer.Printer().print_with_status("Unknown option/s supplied, Type `update help` for more info.", 2)
                return 2
                
        except IndexError:
            self.logger.info("No options supplied.")
            printer.Printer().print_with_status("No option/s supplied. Type `update help` for more info.", 2)
            return 2
    
    def main(self):
        """
        def main():
            The main method of MainClass() class.
        """
        
        self.logger.info("main() method called by {0}().".format(sys._getframe().f_back.f_code.co_name))
        
        # Start the interactive shell.
        self.logger.info("Starting interactive shell...")
        
        print(self.PROGRAM_BANNER)
        print('"' + quote.quote() + '"')
        print()
        while self.byebye is False:
            try:
                # print(config_handler.ConfigHandler(self.configfile).get())  # DEV0005
                self.command = str(input(self.substitute(self.prompt_main)))
                self.latest_error_code = self.parse_command(self.command)
                
            except(KeyboardInterrupt, EOFError):
                self.logger.warning("CTRL+C and/or CTRL+D detected, forcing to quit...")
                self.latest_traceback = traceback.format_exc()
                printer.Printer().print_with_status("CTRL+C and/or CTRL+D detected, forcing {0} to quit...".format(
                    self.PROGRAM_NAME), 1)
                return 1
            
            except BaseException as error:
                self.latest_traceback = traceback.format_exc()
                printer.Printer().print_with_status("An unknown error occured:", 2)
                print(str(error))
                print(self.latest_traceback)
                return 10
                
        else:
            self.logger.info("byebye is True, now quitting...")
            print(quote.quote())
            return 0

# If running independently, run main() function.
if __name__ == '__main__':
    exit_code = 999
    try:
        exit_code = MainClass().main()
    
    except BaseException as MainError:
        traceback.print_exc()
        try:
            with open("data/traceback.log", 'w') as fopen:
                fopen.write('')
                fopen.write(traceback.format_exc())
                
        except(IOError, IsADirectoryError, EOFError, PermissionError):
            pass
        
    try:
        sys.exit(exit_code)

    except SystemExit:
        os._exit(exit_code)
        