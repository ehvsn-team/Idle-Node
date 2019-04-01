#!/usr/bin/env python

# Import directives
try:
    import os
    import sys
    import time
    import traceback
    
    import socket
    import requests
    
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
2 = Unknown command entered
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
        self.PROGRAM_VERSION = "0.0.0.1"
        self.PROGRAM_DESCRIPTION = "An open-source command-line messaging platform"
        self.PROGRAM_BANNER = """\
        _ ___  _    ____    _  _ ____ ___  ____ 
        | |  \ |    |___ __ |\ | |  | |  \ |___ 
        | |__/ |___ |___    | \| |__| |__/ |___ {1}
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
        
        self.logger.info("initialize() method called.")
        
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
        # User details.
        self.logger.info("Getting username...")
        self.username = config_handler.ConfigHandler(self.configfile).get("username")
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, "Starting {0}...".format(self.PROGRAM_NAME), "loading", 0.15)
        self.logger.info("Getting userpass...")
        self.userpass = config_handler.ConfigHandler(self.configfile).get("userpass")
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, "Starting {0}...".format(self.PROGRAM_NAME), "loading", 0.15)
        self.logger.info("Getting user IP Address...")
        self.userip = requests.get('https://api.ipify.org/').text
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
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(True, "Starting {0}...".format(self.PROGRAM_NAME), "loading", 0.15)
        print("Starting {0}... Done!".format(self.PROGRAM_NAME))
        
    def substitute(self, string):
        """
        def substitute():
            Replace strings with the current value.
        """
        
        result = string.replace("$USERNAME", self.username).replace("$USERIP", self.userip)
        result = result.replace("$RECVNAME", self.recvname).replace("$RECVIP", self.recvip)
        result = result.replace("$GCNAME", self.gcname).replace("$GCIP", self.gcip)
        
        return result
    
    def help(self, what="main"):
        """
        def help():
            Return help string.
        """
        
        if what == "main":
            return """\
help | ?                            Show this help menu.
exit | quit | bye | shutdown        Quit {0}.""".format(self.PROGRAM_NAME)

        else:
            raise ValueError("Unknown string is passed to help method.")
    
    def parse_command(self, command):
        """
        def parse_command():
            Parse the command.
        """
        
        # DEV0003
        if command.lower().startswith(("help", "?")):
            print(self.help())
            print()
            return 0
        
        elif command.lower().startswith(("exit", "quit", "bye", "shutdown")):
            self.byebye = True
            return 0
        
        else:
            printer.Printer().print_with_status("Unknown command `{0}`!".format(command), 2)
            print()
            return 2
    
    def main(self):
        """
        def main():
            The main method of MainClass() class.
        """
        
        self.logger.info("main() method called.")
        
        # Start the interactive shell.
        self.logger.info("Starting interactive shell...")
        
        print(self.PROGRAM_BANNER)
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
            print("Goodbye!")
            return 0

# If running independently, run main() function.
if __name__ == '__main__':
    exit_code = MainClass().main()
    try:
        sys.exit(exit_code)

    except SystemExit:
        os._exit(exit_code)
        