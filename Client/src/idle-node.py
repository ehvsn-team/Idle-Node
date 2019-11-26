#!/usr/bin/env python

# Import directives
try:
    import os
    import sys
    import time
    import random
    import signal
    import platform
    import importlib
    import traceback

    # For networking
    import socket
    import requests

    # NOTE: The Tkinter module is imported on the command-line arguments evaluation.

    # For hiding sensitive information while typing
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
    from core import comms_manager
    from core import config_handler

    # DEV0004: For encrypting and decrypting
    from core.Ciphers import aes
    from core.Ciphers import rsa

    # Modules from other sources that is not available
    # on Python repository

    # By kelvinss (source: https://github.com/kelvinss/no-ip-updater)
    from core import no_ip_updater

    # By Ran Aroussi (source: https://github.com/ranaroussi/multitasking)
    from core import multitasking

except ImportError:
    # Prints if error is encountered while importing modules.
    print("[E] Import Error! The program cannot continue...")
    print()
    print("==================== TRACEBACK ====================")
    traceback.print_exc()
    print("===================================================")
    print()
    print("[i] Please contact the author of the program and send this traceback.")
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
8 = DDNS record is not the same as the value in self.userip!
9 = DDNS update Error
10 = Unknown error occured.
11 = self.ddns_provider contains an unknown value
12 = Invalid configuration file (Config file is decrypted or corrupted)
13 = Unknown command-line argument
14 = peer/recipient/server is online, but refused to connect.

"""

"""
config.dat and real_config.dat contents:

first_run              ::  `True` or `False`  ::  True is the program is not yet started. Otherwise, it is set to False.
ip_list                ::  a string           ::  The path of the contact list file.
username               ::  a string           ::  The user's username.
userid                 ::  a string           ::  A random string generated on startup.
userpass               ::  an SHA-1 hash      ::  The user's hashed password.
prompt_main            ::  a string           ::  The string that will show in the main menu prompt.
prompt_p2p_chat        ::  a string           ::  The string that will show when chatting with peers.
prompt_gc_chat         ::  a string           ::  The string that will show when chatting on a conference room.
prompt_settings_panel  ::  a string           ::  The string that will show when on the settings panel.
prompt_benchmark       ::  a string           ::  The string that will show when benchmarking.
ddns                   ::  `True` or `False`  ::  True if user uses a DDNS service. Otherwise, it is set to False.
ddns_provider          ::  a string           ::  The DDNS provider's name.
ddns_domain            ::  a string           ::  The user's DDNS domain given by the DDNS provider.
ddns_token             ::  a string           ::  The user's DDNS token/API key/password given by the DDNS provider.
ping_port              ::  an integer 1~65535 ::  The port that the program will use for recieving ping requests.
sending_port           ::  an integer 1~65535 ::  The port that the program will use for sending messages
recieve_port           ::  an integer 1~65535 ::  The port that the program will use for recieving messages
dedicated_server_ports ::  an integer range   ::  Range of ports that program will use if running as dedicated server.
trans_plaintext        ::  `True` or `False`  ::  If True, it can be used for transporting messages. This is not recommended
trans_base64           ::  `True` or `False`  ::  If True, this cipher can be used for transporting messages.
trans_aes              ::  `True` or `False`  ::  If True, this cipher can be used for transporting messages.
trans_rsa              ::  `True` or `False`  ::  If True, this cipher can be used for transporting messages.
trans_aes_rsa_hybrid   ::  `True` or `False`  ::  If True, this cipher can be used for transporting messages.
trans_third_party      ::  `True` of `False`  ::  If True, third-party ciphers can be used.
save_conversation_logs ::  `True` or `False`  ::  If True, program will save conversation logs on data/conv_logs.dat
max_threads            ::  an integer         ::  Number of threads to use
requests_timeout       ::  an integer         ::  The timeout (in seconds) for requests module.
keypath                ::  a string           ::  The path where the keys are stored.
"""

class MainClass(object):
    """
    MainClass():
        This is the main class of the program.
    """

    def __init__(self, kwargs):
        """
        def __init__():
            This is the initialization method of MainClass() class.
        """

        # Define high-priority variables.
        self.logfile = kwargs.get("logfile", 'data/logfile.log')
        self.configfile = kwargs.get("configfile", 'data/config.dat')

        # Start the logger.
        self.logger = logger.LoggingObject(
                name='Idle-Node',
                logfile=self.logfile
                )

        self.logger.set_logging_level('NOTSET')

        self.start_time = time.time()
        self.logger.info("Running program on {0}...".format(time.ctime(self.start_time)))

        # Get the global variables.
        self.logger.info("Getting global variables...")
        global STARTED

        # Define program variables.
        self.logger.info("Defining program variables...")
        self.PROGRAM_NAME = "Idle-Node"
        self.PROGRAM_VERSION = "0.0.0.7"
        self.PROGRAM_DESCRIPTION = "An open-source decentralized messaging platform"
        self.PROGRAM_BANNER = """\
        _ ___  _    ____    _  _ ____ ___  ____
        | |  \ |    |___ __ |\ | |  | |  \ |___
        | |__/ |___ |___    | \| |__| |__/ |___ v{1}
    {0}""".format(self.PROGRAM_DESCRIPTION, self.PROGRAM_VERSION)

        self.simplelib = simplelib.SimpleLib()

        self.non_symbols = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                           'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                           'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                           'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
                           'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                           'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V' ,'W', 'X',
                           'Y', 'Z']

        self.symbols = ['!', '@', '#', '$', '%', '^', '&', '*',
                           '(', ')', '-', '_', '=', '+', '[', '{', ']', '}',
                           ';', ':', '\'', '"', '\\', '|', ',', '<', '.', '>',
                           '', '/', '?']

        # Check if STARTED is False.
        # If false, initialize program.
        self.logger.info("Checking if STARTED is False...")
        if STARTED == False:
            self.logger.info("STARTED is False, calling initialize() method...")
            self.logger.info("Getting command-line arguments...")
            self.arguments = {}
            self.arguments["override_pyvercheck"] = kwargs.get("override_pyvercheck", False)
            self.arguments["debug_mode"] = kwargs.get("debug_mode", False)
            self.arguments["no-gui"] = kwargs.get("no-gui", False)
            signal.signal(signal.SIGINT, self.cleanup)  # Kill threads on CTRL + C.
            self.initialize(None)

        else:
            self.logger.info("STARTED is True, skipping initialization...")

        # If no-gui argument is True, use shell instead.
        # DEV0002: Please test this first!
        if self.arguments["no-gui"] == True:
            self.logger.debug(self.arguments["no-gui"])
            self.logger.info("GUI is Disabled.")
            ansi.set_title(self.PROGRAM_NAME)

        else:
            self.logger.debug(self.arguments["no-gui"])
            self.logger.info("Creating GUI instance...")
            self.gui = {}
            self.gui["main_scr"] = tkinter.Tk()
            self.logger.info("Setting title...")
            self.gui["main_scr_label"] = tkinter.Label(self.gui["main_scr"], text="{0} v{1} -- {2}".format(self.PROGRAM_NAME, self.PROGRAM_VERSION, self.PROGRAM_DESCRIPTION))
            self.gui["main_scr_label"].mainloop()

        self.sockets = {}
        # Start listening on the redirection port.
        self.sockets['main'] = comms_manager.Main("MainConnection", self.logger, max_threads=self.max_threads, redirection_port=self.redirection_port)
        self.sockets['main'].activate_redirection_port()

        __end_time = time.time()
        __init_time = __end_time - self.start_time
        self.logger.info("Program finished initializing on {0} ({1} seconds to finish initialization)".format(time.ctime(__end_time), __init_time))
        del __end_time
        del __init_time

    def initialize(self, prompt=None):
        """
        def initialize():
            Initialize the program.
        """

        self.logger.info("initialize() method called by {0}().".format(sys._getframe().f_back.f_code.co_name))
        if prompt == None:
            prompt = "Starting {0}...".format(self.PROGRAM_NAME)

        self.logger.info("Evaluating command-line arguments...")
        if self.arguments["debug_mode"] == True:
            self.logger.enable_logging()

        self.logger.info("User uses {0}.".format(platform.python_implementation()))
        self.logger.debug("self.arguments['override_pyvercheck']: {0}".format(self.arguments['override_pyvercheck']))
        if self.arguments['override_pyvercheck'] == False:
            if platform.python_implementation() != 'CPython':
                printer.Printer().print_with_status("You are not using CPython!", 1)
                printer.Printer().print_with_status("{0} in {1} is not yet tested. YOU MIGHT ENCOUNTER BUGS.".format(self.PROGRAM_NAME, platform.python_implementation()), 1)
                time.sleep(3)

            pyversion = sys.version_info
            self.logger.info("User uses {0} v{1}.{2}.{3}".format(platform.python_implementation(), pyversion[0], pyversion[1], pyversion[2]))
            if pyversion[0] < 3 and pyversion[1] < 4 and pyversion[2] < 4:
                printer.Printer().print_with_status("This version of python is not supported!", 1)
                printer.Printer().print_with_status("You have `v{0}.{1}.{2}`. To run {3}, you must have CPython `v3.6.0`.".format(
                    pyversion[0], pyversion[1], pyversion[2], self.PROGRAM_NAME), 1)
                time.sleep(1)

                try:
                    self.cleanup(7)
                    sys.exit(7)

                except SystemExit:
                    os._exit(7)

            if pyversion[0] < 3 and pyversion[1] < 6 and pyversion[2] < 0:
                printer.Printer().print_with_status("This version of Python is supported but we recommend that you use Python v3.6.0+!", 1)
                time.sleep(1)

            del pyversion

        self.logger.info("Getting program data...")
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, prompt, "loading", 0.15)
        # Get program data.
        # Get the list of IPs.
        self.logger.info("Getting IP list...")
        self.contact_list = config_handler.ConfigHandler(self.configfile).get("ip_list")
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, prompt, "loading", 0.15)
        # Get prompts
        # Main prompt
        self.logger.info("Getting main prompt...")
        self.prompt_main = config_handler.ConfigHandler(self.configfile).get("prompt_main")
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, prompt, "loading", 0.15)
        # Prompt when using Peer-to-Peer chat.
        self.logger.info("Getting peer-to-peer prompt...")
        self.prompt_p2p_chat = config_handler.ConfigHandler(self.configfile).get("prompt_p2p_chat")
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, prompt, "loading", 0.15)
        # Prompt when using Group Chat/Conference Room.
        self.logger.info("Getting group chat/conference room prompt...")
        self.prompt_gc_chat = config_handler.ConfigHandler(self.configfile).get("prompt_gc_chat")
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, prompt, "loading", 0.15)
        # Prompt when benchmarking
        self.logger.info("Getting benchmarking prompt...")
        self.prompt_benchmark = config_handler.ConfigHandler(self.configfile).get("prompt_benchmark")
        # Prompt when editing config files.
        self.logger.info("Getting settings/config panel prompt...")
        self.prompt_settings_panel = config_handler.ConfigHandler(self.configfile).get("prompt_settings_panel")
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, prompt, "loading", 0.15)

        # User details.
        self.logger.info("Getting username...")
        self.username = config_handler.ConfigHandler(self.configfile).get("username")
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, prompt, "loading", 0.15)
        self.logger.info("Getting user ID...")
        self.userid = config_handler.ConfigHandler(self.configfile).get("userid")
        self.logger.info("Getting userpass...")
        self.userpass = config_handler.ConfigHandler(self.configfile).get("userpass")

        self.logger.info("Getting requests timeout...")
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, prompt, "loading", 0.15)
        self.requests_timeout = config_handler.ConfigHandler(self.configfile).get("requests_timeout")
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, prompt, "loading", 0.15)
        self.logger.info("Getting user IP Address...")
        try:
            self.userip = requests.get('https://api.ipify.org/', timeout=self.requests_timeout).text

        except(socket.gaierror, requests.packages.urllib3.exceptions.NewConnectionError,
               requests.packages.urllib3.exceptions.MaxRetryError,
               requests.exceptions.ConnectionError):
            self.latest_traceback = traceback.format_exc()
            self.logger.error("An error occured while getting user's IP Address.")
            self.userip = ""

        else:
            self.logger.info("User's IP Address is `{0}`.".format(self.userip))

        self.logger.info("Getting ports...")
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, prompt, "loading", 0.15)
        self.redirection_port = 30000
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, prompt, "loading", 0.15)
        self.ping_port = config_handler.ConfigHandler(self.configfile).get("ping_port")
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, prompt, "loading", 0.15)
        self.sending_port = config_handler.ConfigHandler(self.configfile).get("sending_port")
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, prompt, "loading", 0.15)
        self.recieve_port = config_handler.ConfigHandler(self.configfile).get("recieve_port")

        self.logger.info("Getting Cipher to use on transportation...")
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, prompt, "loading", 0.15)
        self.transportation_ciphers = {}
        self.transportation_ciphers["plaintext"] = config_handler.ConfigHandler(self.configfile).get("trans_plaintext")
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, prompt, "loading", 0.15)
        self.transportation_ciphers["base64"] = config_handler.ConfigHandler(self.configfile).get("trans_base64")
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, prompt, "loading", 0.15)
        self.transportation_ciphers["aes"] = config_handler.ConfigHandler(self.configfile).get("trans_aes")
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, prompt, "loading", 0.15)
        self.transportation_ciphers["rsa"] = config_handler.ConfigHandler(self.configfile).get("trans_rsa")
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, prompt, "loading", 0.15)
        self.transportation_ciphers["aes-rsa-hybrid"] = config_handler.ConfigHandler(self.configfile).get("trans_aes_rsa_hybrid")
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, prompt, "loading", 0.15)
        self.keypath = config_handler.ConfigHandler(self.configfile).get("keypath")

        self.logger.info("Checking if we will save conversation logs...")
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, prompt, "loading", 0.15)
        self.save_conv_logs = config_handler.ConfigHandler(self.configfile).get("save_conversation_logs")

        self.logger.info("Getting and setting max threads.")
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, prompt, "loading", 0.15)
        self.max_threads = config_handler.ConfigHandler(self.configfile).get("max_threads")
        if self.max_threads == 0:
            self.logger.debug("Max threads: {0}".format(multitasking.config["CPU_CORES"] * 5))
            multitasking.set_max_threads(multitasking.config["CPU_CORES"] * 5)

        else:
            self.logger.debug("Max threads: {0}".format(self.max_threads))
            multitasking.set_max_threads(self.max_threads)

        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, prompt, "loading", 0.15)
        self.logger.info("Setting chat placeholders...")
        self.recvname = ""
        self.recvpass = ""
        self.recvip = ""
        self.gcname = ""
        self.gcpass = ""
        self.gcip = ""
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, prompt, "loading", 0.15)
        self.logger.info("Setting latest traceback placeholder...")
        self.latest_traceback = ""
        self.latest_error_code = 0
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, prompt, "loading", 0.15)
        self.logger.info("Setting command placeholder...")
        self.command = ""
        asciigraphs.ASCIIGraphs().animated_loading_screen_manual(False, prompt, "loading", 0.15)
        self.logger.info("Setting main method loop...")
        self.byebye = False

        self.logger.info("Finished loading!")
        if prompt.endswith('.'):
            asciigraphs.ASCIIGraphs().animated_loading_screen_manual(True, "{0} Done!".format(prompt), "loading", 0.15)

        else:
            asciigraphs.ASCIIGraphs().animated_loading_screen_manual(True, "{0}... Done!".format(prompt), "loading", 0.15)

        self.logger.info("first_run value is `{0}`.".format(config_handler.ConfigHandler(self.configfile).get("first_run")))
        self.logger.debug(config_handler.ConfigHandler(self.configfile).get("first_run"))
        self.logger.debug(type(config_handler.ConfigHandler(self.configfile).get("first_run")))
        if config_handler.ConfigHandler(self.configfile).get("first_run") == True:
            config_handler.ConfigHandler(self.configfile).set("userid", self.simplelib.prsg(10, self.non_symbols))
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
            print()
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
                        self.logger.info("User skipped first run wizard.")
                        printer.Printer().print_with_status("Type `first_run` in the main terminal to run this wizard.", 0)
                        return self.save_settings2config(True, "Anonymous{0}".format(random.randint(0, 10000)), "", False, "None", "None", "None")

                except(KeyboardInterrupt, EOFError):
                    continue

            while True:
                try:
                    username = input("Username: ")
                    for char in username:
                        if char.isalpha() or char.isdigit() or char == '_':
                            approved = True
                            continue

                        else:
                            approved = False
                            continue

                    if approved == True:
                        pass

                    else:
                        self.logger.error("User entered an invalid username.")
                        printer.Printer().print_with_status("Your username must consist of letters, numbers, or an underscore!", 2)
                        continue

                    if len(username) <= 6 or len(username) > 20:
                        self.logger.error("User entered an invalid username.")
                        printer.Printer().print_with_status("Your username must be atleast 6~20 characters!")
                        continue

                    else:
                        self.logger.info("User entered an accepted username.")
                        break

                except(KeyboardInterrupt, EOFError):
                    continue

            while True:
                try:
                    userpass = getpass("Password: ")
                    self.logger.info("User created a new password.")
                    if self.check_password(userpass) == 0:
                        pass

                    else:
                        continue

                    checkpass = getpass("Confirm Password: ")
                    self.logger.info("User is confirming the password...")
                    if userpass == checkpass:
                        userpass = self.hashit(userpass)
                        self.logger.info("Both passwords matched!")
                        break

                    else:
                        self.logger.error("Both passwords does not match.")
                        printer.Printer().print_with_status("Both passwords does not match!", 2)
                        continue

                except(KeyboardInterrupt, EOFError):
                    continue

            while True:
                try:
                    self.logger.info("Asking user if needs DDNS.")
                    print("Do you need a DDNS?")
                    print("(DDNS is usually used if you have a dynamic IP.)")
                    printer.Printer().print_with_status("For more info, search on your favorite search engine.", 0)
                    use_ddns = input("Answer (y/n): ")
                    if use_ddns.lower() == 'y':
                        self.logger.info("User will need a DDNS.")
                        use_ddns = True
                        break

                    elif use_ddns.lower() == 'n':
                        use_ddns = False
                        ddns_provider = "None"
                        ddns_domain = "None"
                        ddns_token = "None"
                        self.logger.info("User does not need a DDNS.")
                        break

                    else:
                        self.logger.info("Unknown answer.")
                        continue

                except(KeyboardInterrupt, EOFError):
                    continue

            if use_ddns == True:
                print("Supported DDNS Providers:")
                print("    -DuckDNS.org        -noip.com")
                print()
                printer.Printer().print_with_status("Please contact us if your favorite DDNS provider is not listed above!", 0)
                print()
                while True:
                    try:
                        self.logger.info("Asking user what DDNS provider we will use...")
                        ddns_provider = input("Please enter your DDNS Provider (Ex.: `duckdns.org` or simply `duckdns`): ")
                        self.logger.info("User entered `{0}`.".format(ddns_provider))

                        if "duckdns" in ddns_provider.lower():
                            self.logger.info("DDNS Provider matched DuckDNS.org")
                            ddns_provider = "DuckDNS"
                            break

                        elif "noip" in  ddns_provider.lower():
                            self.logger.info("DDNS Provider matched noip.com")
                            ddns_provider = "noip"
                            break

                        else:
                            self.logger.info("DDNS Provider does not match to any supported DDNS Providers.")
                            continue

                    except(TypeError, ValueError, EOFError, KeyboardInterrupt):
                        self.latest_traceback = traceback.format_exc()
                        continue

            else:
                pass

            if use_ddns == True:
                if ddns_provider == "DuckDNS":
                    while True:
                        try:
                            self.logger.info("Asking user for DuckDNS.org domain name...")
                            ddns_domain = input("Enter your DuckDNS.org domain name: ")
                            self.logger.info("Asking user for DuckDNS.org token...")
                            ddns_token = input("Enter your DuckDNS.org token: ")
                            break

                        except(KeyboardInterrupt, EOFError):
                            continue

                elif ddns_provider == "noip":
                    while True:
                        try:
                            self.logger.info("Asking for noip.com domain name...")
                            ddns_domain = input("Enter your noip.com domain name: ")
                            self.logger.info("Asking for noip.com username...")
                            ddns_username = input("Enter your noip.com username: ")
                            self.logger.info("Asking for noip.com password...")
                            ddns_userpass = getpass("Enter your noip.com password: ")
                            ddns_token = ddns_username + ':::' + ddns_userpass
                            del ddns_username
                            del ddns_userpass
                            break

                        except(KeyboardInterrupt, EOFError):
                            continue

                else:
                    self.logger.error("use_ddns is True but no DDNS Provider matched!")
                    printer.Printer().print_with_status("Unknown DDNS provider!", 2)
                    return 6

        except(TypeError, ValueError):
            self.logger.error("An error occured when starting the First-run wizard.")
            printer.Printer().print_with_status("An error occured when starting the First-run wizard.", 2)
            self.latest_traceback = traceback.format_exc()
            return 10

        else:
            self.logger.info("Generating primary RSA keys...")
            printer.Printer().print_with_status("Generating primary RSA keys...")
            if rsa.Main().generate_key(self.keypath + "main.pem") == 0:
                pass

            else:
                self.latest_traceback = traceback.format_exc()
                printer.Printer().print_with_status("An unknown error occured while generating your primary RSA key. Please try again later.")

            self.logger.info("Saving settings to configuration file...")

            self.save_settings2config(True, username, userpass, use_ddns, ddns_provider, ddns_domain, ddns_token)
            return 0

    def save_settings2config(self, load_settings=True, username="Anonymous", userpass="", use_ddns=None, ddns_provider=None, ddns_domain=None, ddns_token=None):
        """
        def save_settings2config():
            Save settings to configuration file...
            Well, the method name is self-explanatory...
        """

        self.logger.info("save_settings2config() method called by {0}().".format(sys._getframe().f_back.f_code.co_name))

        # How many settings do we have to save?
        total_items = 6

        """
config.dat and real_config.dat contents:

first_run              ::  `True` or `False`  ::  True is the program is not yet started. Otherwise, it is set to False.
ip_list                ::  a string           ::  The path of the contact list file.
username               ::  a string           ::  The user's username.
userid                 ::  a string           ::  A random string generated on startup.
userpass               ::  an SHA-1 hash      ::  The user's hashed password.
prompt_main            ::  a string           ::  The string that will show in the main menu prompt.
prompt_p2p_chat        ::  a string           ::  The string that will show when chatting with peers.
prompt_gc_chat         ::  a string           ::  The string that will show when chatting on a conference room.
prompt_settings_panel  ::  a string           ::  The string that will show when on the settings panel.
ddns                   ::  `True` or `False`  ::  True if user uses a DDNS service. Otherwise, it is set to False.
ddns_provider          ::  a string           ::  The DDNS provider's name.
ddns_domain            ::  a string           ::  The user's DDNS domain given by the DDNS provider.
ddns_token             ::  a string           ::  The user's DDNS token/API key/password given by the DDNS provider.
ping_port              ::  an integer 1~65535 ::  The port that the program will use for recieving ping requests.
sending_port           ::  an integer 1~65535 ::  The port that the program will use for sending messages
recieve_port           ::  an integer 1~65535 ::  The port that the program will use for recieving messages
dedicated_server_ports ::  an integer range   ::  Range of ports that program will use if running as dedicated server.
trans_plaintext        ::  `True` or `False`  ::  If True, it can be used for transporting messages. This is not recommended
trans_base64           ::  `True` or `False`  ::  If True, this cipher can be used for transporting messages.
trans_aes              ::  `True` or `False`  ::  If True, this cipher can be used for transporting messages.
trans_rsa              ::  `True` or `False`  ::  If True, this cipher can be used for transporting messages.
trans_aes_rsa_hybrid   ::  `True` or `False`  ::  If True, this cipher can be used for transporting messages.
trans_third_party      ::  `True` of `False`  ::  If True, third-party ciphers can be used.
save_conversation_logs ::  `True` or `False`  ::  If True, program will save conversation logs on data/conv_logs.dat
max_threads            ::  an integer         ::  Number of threads to use
requests_timeout       ::  an integer         ::  The timeout (in seconds) for requests module.
keypath                ::  a string           ::  The path where the keys are stored.
        """

        try:
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
            self.logger.info("Finished saving settings to configuration file!")
            self.logger.info("Updating values...")
            if load_settings == True:
                self.initialize("Updating values...")

            return 0

        except Exception as err:
            self.latest_traceback = traceback.format_exc()
            self.logger.error("An error occured while saving setting. (error on next log line.)")
            self.logger.error(str(err))
            return 1

    def hashit(self, string, cipher="sha256"):
        """
        def hashit():
            Return the hash of the string.
        """

        return self.simplelib.hash(string, cipher)

    def get_task_number(self):
        """
        def get_task_number():
            Get running tasks (threads/processes) and maximum tasks.

        """

        tasks = 0
        max_tasks = 0

        tasks = multitasking.config['TASKS'] + comms_manager.multitasking.config['TASKS']
        max_threads = multitasking.config['MAX_THREADS'] + comms_manager.multitasking.config['MAX_THREADS']

        return (tasks, max_threads)

    def update_ddns_service(self):
        """
        def update_ddns_service():
            Update DDNS if user uses one.
        """

        self.logger.info("update_ddns_service() method called by {0}().".format(sys._getframe().f_back.f_code.co_name))
        if config_handler.ConfigHandler(self.configfile).get("ddns") == True:
            self.logger.info("Updating DDNS Service...")
            if config_handler.ConfigHandler(self.configfile).get("ddns_provider") == "DuckDNS":
                try:
                    self.logger.info("Updating DuckDNS.org Domain...")
                    duckdns_recv = requests.get("https://www.duckdns.org/update?domains={0}&token={1}&ip={2}&verbose=true".format(
                        config_handler.ConfigHandler(self.configfile).get("ddns_domain"),
                        config_handler.ConfigHandler(self.configfile).get("ddns_token"),
                        self.userip)).text

                    duckdns_recv = duckdns_recv.split('\n')
                    self.logger.debug(duckdns_recv)
                    if duckdns_recv[0] == "OK":
                        if duckdns_recv[1] == self.userip:
                            if duckdns_recv[3] == "UPDATED":
                                self.logger.info("No problems are encountered when updating DDNS.")
                                return 0

                            elif duckdns_recv[3] == "NOCHANGE":
                                self.logger.warning("DuckDNS returns `NOCHANGE`. Record is not updated.")
                                return 0

                            else:
                                self.logger.warning("DuckDNS returns an unknown value `{0}`.".format(duckdns_recv[3]))
                                return 0

                        else:
                            self.logger.warning("DuckDNS record is not the same as the value in self.userip!")
                            return 8

                    else:
                        self.logger.error("KO! KO! DuckDNS replies.")
                        return 9

                except(socket.gaierror, requests.packages.urllib3.exceptions.NewConnectionError,
                   requests.packages.urllib3.exceptions.MaxRetryError,
                   requests.exceptions.ConnectionError):
                    self.latest_traceback = traceback.format_exc()
                    self.logger.error("An error occured while updating DDNS.")
                    return 10

            elif config_handler.ConfigHandler(self.configfile).get("ddns_provider") == "noip":
                try:
                    self.logger.info("Updating noip.com Domain...")
                    no_ip_updater.update(config_handler.ConfigHandler(self.configfile).get("ddns_token").partition(':::')[0], config_handler.ConfigHandler(self.configfile).get("ddns_token").partition(':::')[2], config_handler.ConfigHandler(self.configfile).get("ddns_domain"), self.userip)

                except urllib.error.HTTPError as e:
                    printer.Printer().print_with_status("An error occured when updating noip domain:", 2)
                    printer.Printer().print_with_status(str(e))
                    return 9

                except BaseException as error:
                    self.latest_traceback = traceback.format_exc()
                    self.logger.error("An error occured while updating DDNS.")
                    return 10

            elif config_handler.ConfigHandler(self.configfile).get("ddns_provider") == "None":
                self.logger.info("Skipping DDNS update, ddns_provider is None.")
                return 0

            else:
                self.logger.error("self.ddns_provider contains an unknown value: `{0}`".format(config_handler.ConfigHandler(self.configfile).get("ddns_provider")))
                return 11

        else:
            self.logger.info("User does not use DDNS service. Using IP address as the identity of the user.")
            return 0

    def check_password(self, password, username=None):
        """
        def check_password():
            Check the password and give suggestions.
        """

        if username is None:
            username = self.username

        if len(password) < 6:
            printer.Printer().print_with_status("Your password must be atleast 6 characters!", 2)
            self.logger.error("User's password is not long enough.")
            return 1

        else:
            self.logger.info("Checking for password strength....")
            if len(password) <= 8:
                print("Password Strength: Bad")
                self.logger.info("Password Strength: Bad")

            elif len(password) > 8 and len(password) <= 12:
                print("Password Strength: OK")
                self.logger.info("Password Strength: OK")

            elif len(password) > 12 and len(password) <= 18:
                print("Password Strength: Good")
                self.logger.info("Password Strength: Good")

            else:
                print("Password Strength: Better")
                self.logger.info("Password Strength: Better")

            if password.lower() == username.lower():
                print("You must not use your username as your password!")
                return 2

            if password.isalpha():
                print("[SUGGESTION]: Your password must have numbers and symbols.")

            elif password.isdigit():
                print("[SUGGESTION]: Your password must have letters and symbols.")

            for char in password:
                if char in "[ !#$%&'()*+,-./[\\\]^_`{|}~\"]":
                    symbol_only = True

                else:
                    symbol_only = False

            if symbol_only == True:
                print("[SUGGESTION]: Your password must have letters and numbers.")

            del symbol_only

        return 0

    def substitute(self, string):
        """
        def substitute():
            Replace strings with the current value.
        """

        string = str(string)
        self.logger.info("substitute() method called by {0}().".format(sys._getframe().f_back.f_code.co_name))
        result = string.replace("$USERNAME", self.username).replace("$USERIP", self.userip)
        result = result.replace("$RECVNAME", self.recvname).replace("$RECVIP", self.recvip)
        result = result.replace("$GCNAME", self.gcname).replace("$GCIP", self.gcip)

        self.logger.info("Returning substituted string.")
        return result

    def help(self, what="main"):
        """
        def help():
            Return help string.
        """

        self.logger.info("help() method called by {0}().".format(sys._getframe().f_back.f_code.co_name))
        if what == "main":
            self.logger.info("Returning {0} help menu...".format(what))
            return """\
help | ?                            Show this help menu.
config | settings                   Access the Settings/Customization Panel.
update [OPTION]                     Update status of [OPTION]. (Type `update ?` for more info.)
status                              Show {0}'s current status.
contacts | cntcts                   Contacts manager.
benchmark | bench                   Benchmark cipher algorithms.
first_run                           Start the first-run wizard.
clrscrn | cls | clr                 Clear the contents of the screen.

trace                               Show the latest traceback.

exit | quit | bye | shutdown        Quit {0}.""".format(self.PROGRAM_NAME)

        elif what == "config_panel":
            self.logger.info("Returning {0} help menu...".format(what))
            return """\
help | ?                    Show this help menu.
show                        List configuration values.
set [OPTION] [VALUE]        Set the value for `OPTION`. (NOTE: DO NOT ENTER VALUE WHEN SETTING PASSWORD!)
discard [OPTION]            Discard changes made to `OPTION`.
save                        Save current settings to configuration file.
clrscrn | cls | clr         Clear the contents of the screen.

back                        Exit the Settings panel."""

        elif what == "update":
            self.logger.info("Returning {0} help menu...".format(what))
            return """\
help | ?        Show this help menu.
ip              Update YOUR IP Address.
ddns            Update YOUR DDNS domain. (If you use one.)
"""

        elif what == "cntcts":
            self.logger.info("Returning {0} help menu...".format(what))
            return """\
help | ?        Show this help menu.
add | new       Add a new contact on-line or off-line.
"""

        else:
            self.logger.error("Unknown string is passed to help method.")
            printer.Printer().print_with_status("Unknown string is passed to help method!", 2)
            input("Press enter to continue...")
            return ""

    def parse_command(self, command):
        """
        def parse_command():
            Parse the command.
        """

        self.logger.info("parse_command() called by {0}().".format(sys._getframe().f_back.f_code.co_name))
        self.logger.debug(type(command))
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

        elif command.lower().startswith("status"):
            self.logger.info("Showing program's current status.")
            print()
            printer.Printer().print_with_status("{0} STATUS".format(self.PROGRAM_NAME.upper()), 0)
            print()
            printer.Printer().print_with_status("Client Version: {0}".format(self.PROGRAM_VERSION))
            printer.Printer().print_with_status("Uptime: {0}".format("{0}".format(str(self.simplelib.seconds_to_hms(int(time.time() - self.start_time))))))
            print()
            if config_handler.ConfigHandler(self.configfile).get("ddns") == True:
                printer.Printer().print_with_status("Username: {0} ({1})".format(self.username, config_handler.ConfigHandler(self.configfile).get("ddns_domain")))

            else:
                printer.Printer().print_with_status("Username: {0} ({1})".format(self.username, self.userip))

            printer.Printer().print_with_status("User ID: {0}".format(self.userid))
            printer.Printer().print_with_status("Current IP Address: {0}".format(self.userip))
            if config_handler.ConfigHandler(self.configfile).get("ddns") == True:
                printer.Printer().print_with_status("Current DDNS Domain: {0} ({1})".format(config_handler.ConfigHandler(self.configfile).get("ddns_domain"), gethost.byname(config_handler.ConfigHandler(self.configfile).get("ddns_domain"))))

            else:
                printer.Printer().print_with_status("Current DDNS Domain: [DISABLED]")

            print()
            printer.Printer().print_with_status("To let others chat with you, send them your DDNS Domain.", 1)
            printer.Printer().print_with_status("If you are not using a DDNS service, send them your IP Address", 1)
            printer.Printer().print_with_status("But be careful on who you trust!", 1)
            printer.Printer().print_with_status("We recommend that you use a proxy/VPN and a DDNS service to hide your real IP.", 1)
            print()
            printer.Printer().print_with_status("Ping/Latency Port: {0}".format(str(self.ping_port)))
            printer.Printer().print_with_status("Sending Port: {0}".format(str(self.sending_port)))
            printer.Printer().print_with_status("Recieve Port: {0}".format(str(self.recieve_port)))
            print()
            printer.Printer().print_with_status("Save Conversation Logs: {0}".format(str(self.save_conv_logs)))
            print()
            allowed_ciphers = ""
            for cipher in self.transportation_ciphers:
                if self.transportation_ciphers[cipher] == True:
                    allowed_ciphers += "{0} | ".format(cipher)

                else:
                    continue

            allowed_ciphers = allowed_ciphers[::-1]
            allowed_ciphers = allowed_ciphers.partition(" | ")[2]
            allowed_ciphers = allowed_ciphers[::-1]

            printer.Printer().print_with_status("Allowed Ciphers: {0}".format(allowed_ciphers))
            print()
            printer.Printer().print_with_status("Interpreter: {0} v{1}.{2}.{3}".format(platform.python_implementation(), sys.version_info[0], sys.version_info[1], sys.version_info[2]))
            printer.Printer().print_with_status("Debug Mode: {0}".format(self.arguments['debug_mode']))
            printer.Printer().print_with_status("Log File: {0}".format(self.logfile))
            printer.Printer().print_with_status("Configuration File: {0}".format(self.configfile))
            printer.Printer().print_with_status("Maximum Threads: {0} (Real Value: {1} | 0 is default; depends on CPU count.)".format(self.max_threads, multitasking.config['MAX_THREADS']))
            printer.Printer().print_with_status("Running Tasks: {0} (Max: {1})".format(len(multitasking.config['TASKS']) + 1, (multitasking.config['MAX_THREADS'] + 1)))
            print()

        elif command.lower().startswith(("cntcts", "contacts")):
            self.logger.info("Calling contacts_manager() method...")
            return self.contacts_manager(command)

        elif command.lower().startswith(( "benchmark", "bench")):
            self.logger.info("Calling benchmark() method...")
            return self.benchmark()

        elif command.lower().startswith(("first_run",)):
            self.logger.info("Calling first_run() method...")
            return self.first_run()

        elif command.lower().startswith(("cls", "clear", "clr")):
            self.logger.info("Clearing the contents of the screen.")
            self.simplelib.clrscrn()
            return 0

        elif command.lower().startswith(("trace",)):
            print("\nLATEST TRACEBACK:\n")
            print(self.latest_traceback)
            print()
            return 0

        elif command.lower().startswith(("exit", "quit", "bye", "shutdown")):
            self.logger.info("Setting byebye value to True.")
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

                        elif line.startswith(("first_run=", "userid=")):
                            continue

                        elif 'pass' in line.partition('=')[0] or 'token' in line.partition('=')[0]:
                            printer.Printer().print_with_status("{0}: {1}".format(line.partition('=')[0],
                                ('*' * len(line.partition('=')[2]))), 0)

                        elif line.partition('=')[2] == "":
                            printer.Printer().print_with_status("{0}: [NO VALUE]".format(line.partition('=')[0]), 0)

                        elif '=' in line:
                            printer.Printer().print_with_status(line.replace('=', ': '), 0)
                            # self.logger.debug(line.endswith("\n"))  # DEV0005: Just checking if the line ends with a newline.

                        else:
                            continue

                    print()

                elif config_command.lower().startswith(("set")):
                    self.logger.info("Set command called.")
                    try:
                        self.logger.info("Getting option and its value...")
                        option = config_command.split(' ')[1]
                        try:
                            value = config_command.partition(' ')[2].partition(' ')[2]

                        except(IndexError):
                            value = "None"

                    except IndexError:
                        self.latest_traceback = traceback.format_exc()
                        self.logger.error("Cannot get option and value.")
                        printer.Printer().print_with_status("USAGE: set [OPTION] [VALUE]", 2)
                        continue

                    if option.startswith(('#', "first_run", "userid")):
                        self.logger.error("Invalid option supplied.")
                        printer.Printer().print_with_status("Invalid option!", 2)
                        continue

                    elif option == "":
                        self.logger.error("Invalid option supplied.")
                        printer.Printer().print_with_status("Invalid option!", 2)
                        continue

                    else:
                        if 'pass' in option:
                            if len(config_handler.ConfigHandler(self.configfile).get("userpass")) != 0:
                                old_value = str(getpass("Enter the old value for `{0}`: ".format(option)))
                                if self.hashit(old_value) == config_handler.ConfigHandler(self.configfile).get("userpass"):
                                    pass

                                else:
                                    printer.Printer().print_with_status("Both values does not match!", 2)
                                    continue

                                del old_value

                            value = getpass("Please enter your new value for `{0}`: ".format(option))
                            if self.check_password(value) != 0:
                                continue

                            value = self.hashit(value)

                            self.logger.info("Asking user to re-enter the value.")
                            value_verification = self.hashit(str(getpass("Please re-enter your new value for `{0}`: ".format(option))))
                            if value_verification == value:
                                del value_verification

                            else:
                                printer.Printer().print_with_status("Both values does not match!", 2)
                                continue

                        self.logger.info("Checking if value type is the same as the old values type.")
                        if type(config_handler.ConfigHandler(self.configfile).get(option)) is bool:
                            self.logger.info("option needs a boolean value.")
                            if value.lower() == 'true':
                                value = "True"

                            elif value.lower() == 'false':
                                value = "False"

                            elif value.startswith("0"):
                                value = "False"

                            elif value.startswith("1"):
                                value = "True"

                            else:
                                self.logger.error("value is not true/false/0/1!")
                                printer.Printer().print_with_status("Boolean values must be True, False, 0, or 1!", 2)
                                continue

                        elif type(config_handler.ConfigHandler(self.configfile).get(option)) is str:
                            self.logger.info("option needs a string value. Passing.")
                            pass

                        elif type(config_handler.ConfigHandler(self.configfile).get(option)) is int:
                            self.logger.info("option needs an integer value.")
                            try:
                                int(value)

                            except(TypeError, ValueError):
                                self.logger.info("The value was not an integer!")
                                printer.Printer().print_with_status("The option needs an integer value!", 2)
                                continue

                        elif type(config_handler.ConfigHandler(self.configfile).get(option)) is float:
                            self.logger.info("option needs a floating-point value.")
                            try:
                                float(value)
                                if '.' not in str(value):
                                    value = str(value) + '.0'

                            except(TypeError, ValueError):
                                self.logger.info("value is not a floating-point!")
                                printer.Printer().print_with_status("The option needs a floating point value!", 2)
                                continue

                        else:
                            printer.Printer().print_with_status("Option needs an unknown value type!", 2)
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
                        if changed == False:
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
                        self.latest_traceback = traceback.format_exc()
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
                            if changed == False:
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
                            self.logger.debug("{0} {1} {2}".format(config_line.partition('=')[0], '=', config_line.partition('=')[2]))
                            config_handler.ConfigHandler(self.configfile).set(config_line.partition('=')[0], config_line.partition('=')[2])

                    printer.Printer().print_with_status("Saving current settings to configuration file... Done!", 0)
                    self.initialize("Loading new configuration")
                    continue

                elif config_command.lower().startswith(("cls", "clear", "clr")):
                    self.simplelib.clrscrn()

                elif config_command.lower().startswith(("back",)):
                    if config_lines != config_handler.ConfigHandler(self.configfile).get():
                        printer.Printer().print_with_status("You have made changes to the settings!", 1)
                        while True:
                            try:
                                askIfSave = input("Go back and save changes? (y/n) > ")

                            except(TypeError, ValueError, KeyboardInterrupt, EOFError):
                                continue

                            else:
                                if askIfSave.lower() == 'y':
                                    break

                                elif askIfSave.lower() == 'n':
                                    return 0

                                else:
                                    continue

                    else:
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
                    self.userip = requests.get('https://api.ipify.org/', timeout=self.requests_timeout).text

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
                    self.logger.info("User's IP Address is `{0}`.".format(self.userip))
                    printer.Printer().print_with_status("Your IP Address is: `{0}".format(self.userip), 0)
                    return 0

            elif command[1].startswith(("ddns",)):
                self.logger.info("Updating user DDNS...")
                upddns = self.update_ddns_service()
                if upddns == 0:
                    if config_handler.ConfigHandler(self.configfile).get("ddns") == True:
                        printer.Printer().print_with_status("DDNS domain successfully updated!", 0)

                    else:
                        printer.Printer().print_with_status("You are not using a DDNS service, nothing changed!", 1)

                elif upddns == 8:
                    printer.Printer().print_with_status("DDNS record is not the same as the value in self.userip!", 1)

                elif upddns == 9:
                    printer.Printer().print_with_status("An error occured when updating DDNS domain.", 2)

                elif upddns == 11:
                    printer.Printer().print_with_status("The key `ddns_provider` contains an unknown value!", 2)
                    printer.Printer().print_with_status("The DDNS provider ({0}) might not be supported by {1}.".format(
                        config_handler.ConfigHandler(self.configfile).get("ddns_provider"), self.PROGRAM_NAME), 2)

                else:
                    printer.Printer().print_with_status("Program cannot determine the success of the DDNS update. Type `trace` to show latest traceback.", 1)
                pass

            else:
                self.logger.info("Unknown option/s supplied.")
                printer.Printer().print_with_status("Unknown option/s supplied, Type `update help` for more info.", 2)
                return 2

        except IndexError:
            self.latest_traceback = traceback.format_exc()
            self.logger.info("No options supplied.")
            printer.Printer().print_with_status("No option/s supplied. Type `update help` for more info.", 2)
            return 2

    def contacts_manager(self, commands):
        """
        def contacts_manager():
            Manages the contact list.
        """

        self.logger.info("contacts_manager() method called by {0}().".format(sys._getframe().f_back.f_code.co_name))

        commands = commands.split(' ')
        self.logger.info("Commands: {0}".format(str(commands)))
        try:
            command = commands[1]

        except IndexError:
            self.logger.error("Insufficient number of arguments, printing help menu.")
            print(self.help("cntcts"))
            return 0

        self.logger.info("contacts_manager() method called by {0}().".format(sys._getframe().f_back.f_code.co_name))
        if command.lower().startswith(("help", "?")):
            self.logger.info("Printing help menu.")
            print(self.help("cntcts"))
            return 0

        elif command.lower().startswith(("add", "new")):
            self.logger.info("command is `{0}`.".format(command))
            print("[i] Example: user.duckdns.org  |  192.168.0.101")
            peer_address = input("[PEER'S ADDRESS]: ")
            self.logger.info("User entered `{0}` as peer's address".format(peer_address))

            try:
                pass # DEV0003

            except ConnectionRefusedError as e:
                self.latest_traceback = traceback.format_exc()
                self.logger.error("An error occured while connecting to peer: {0}".format(str(e)))
                printer.Printer().print_with_status("`{0}` is online, but no connection could be made because the target machine actively refused it.".format(peer_address), 2)
                return 14

            except Exception as e:
                self.logger.error("Unknown error occured: {0}".format(str(e)))
                printer.Printer().print_with_status("An unknown error occured! (Type `trace` to show latest traceback).")
                self.latest_traceback = traceback.format_exc()
                self.simplelib.pause()
                return 10

            else:
                # Recieve peer's public key or string `denied`.
                try:
                    response = socket_obj.recv(2048)

                except Exception as e:
                    self.logger.error("Unknown error occured: {0}".format(str(e)))
                    printer.Printer().print_with_status("An unknown error occured! (Type `trace` to show latest traceback).")
                    self.latest_traceback = traceback.format_exc()
                    self.simplelib.pause()
                    return 10

                else:
                    # Close the connection.
                    socket_obj.close()

        else:
            self.logger.info("Unknown option supplied, printing help menu.")
            print(self.help("cntcts"))
            return 0

    def cleanup(self, error_code=0, *args):
        """
        def cleanup():
            Do cleanup and return

        """

        multitasking.killall()

        return error_code

    def benchmark(self):
        """
        def benchmark():
            Benchmark cipher algorithms.
        """

        test_key = "0eH-1L&Qt779KNOO"
        test_pubkey = ""
        # DEV0003

        test_string = "This is a test sentence."
        test_string_long = """
This is a long test paragraph.
Please read the Zen of Python by Tim Peters:

The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
        """

        print("Enter `all` to test all cipher algorithms.")
        print("Enter a cipher name to test the specified cipher.")
        print("Enter `list` to list all available cipher algorithms.")
        print()
        while True:
            try:
                command = str(input(self.substitute(self.prompt_main)))
                if command.lower() == "all":
                    printer.Printer().print_with_status("Starting string benchmark...", 1)
                    e_str_benchmarks = {}

                    printer.Printer().print_with_status("Benchmarking AES algorithm...")
                    e_str_benchmarks["AES"] = [time.time(), 0.0, 0.0]
                    aes_test = aes.IdleCipher().encrypt(test_key, test_string)
                    e_str_benchmarks["AES"][1] = time.time()
                    aes.IdleCipher().decrypt(test_key, aes_test)
                    e_str_benchmarks["AES"][2] = time.time()
                    del aes_test

                    printer.Printer().print_with_status("Benchmarking RSA algorithm...")
                    e_str_benchmarks["RSA"] = [time.time(), 0.0, 0.0]
                    rsa_test = rsa

                else:
                    print("Enter `all` to test all cipher algorithms.")
                    print("Enter a cipher name to test the specified cipher.")
                    print("Enter `list` to list all available cipher algorithms.")

            except Exception as e:
                self.latest_traceback = traceback.format_exc()
                printer.Printer().print_with_status("An error occured while benchmarking: {0}".format(str(e)))

            finally:
                print("ENCRYPTION:")
                print("AES: ")
                # DEV0003

    def main(self):
        """
        def main():
            The main method of MainClass() class.
        """

        self.logger.info("main() method called by {0}().".format(sys._getframe().f_back.f_code.co_name))

        # Start the interactive shell or the GUI.
        self.logger.info("Starting interactive shell...")
        print(self.PROGRAM_BANNER)
        print()
        while True:
            try:
                if len(config_handler.ConfigHandler(self.configfile).get("userpass")) != 0:
                    ask4pass = self.hashit(getpass("Please enter your password: "))
                    # DEV0004: Try to decrypt files. If error occured, means wrong password
                    if ask4pass == config_handler.ConfigHandler(self.configfile).get("userpass"):
                        self.simplelib.clrscrn()
                        break

                    else:
                        printer.Printer().print_with_status("You have entered an incorrect password!", 2)
                        self.simplelib.pause()
                        # self.simplelib.clrscrn()
                        continue

                else:
                    break

            except(KeyboardInterrupt, EOFError):
                printer.Printer().print_with_status("You need to enter your password to decrypt your information.")
                print("Do you really want to quit? (y/n)")
                while True:
                    try:
                        quitconfirm = input("[Answer]: ")
                        if quitconfirm.lower() == 'y':
                            return self.cleanup(0)

                        elif quitconfirm.lower() == 'n':
                            break

                        else:
                            continue

                    except(KeyboardInterrupt, EOFError):
                        return self.cleanup(1)

            except Exception as err:
                self.latest_traceback = traceback.format_exc()
                continue

        self.simplelib.clrscrn()
        print(self.PROGRAM_BANNER)
        print('"' + quote.quote() + '"')
        print()
        while self.byebye == False:
            try:
                # self.logger.debug(config_handler.ConfigHandler(self.configfile).get())  # DEV0005: If we let this active, it will be a security issue
                new_command = str(input(self.substitute(self.prompt_main)))
                self.logger.debug(new_command)
                if ' && ' in new_command:
                    self.logger.info("&& characters detected, stripping command.")
                    new_command = new_command.split(" && ")
                    self.logger.debug(new_command)
                    for command in new_command:
                        self.command = command
                        self.latest_error_code = self.parse_command(self.command)

                elif ' || ' in new_command:
                    self.logger.info("|| characters detected, stripping command.")
                    new_command = new_command.split(" || ")
                    self.logger.debug(new_command)
                    for command in new_command:
                        self.command = command
                        self.latest_error_code = self.parse_command(self.command)
                        if self.latest_error_code == 0:
                            continue

                        else:
                            break

                else:
                    self.logger.info("no && and/or || characters detected, not stripping command.")
                    self.logger.debug(new_command)
                    self.command = new_command
                    self.latest_error_code = self.parse_command(self.command)

            except(KeyboardInterrupt, EOFError):
                self.logger.warning("CTRL+C and/or CTRL+D detected, forcing to quit...")
                self.latest_traceback = traceback.format_exc()
                printer.Printer().print_with_status("CTRL+C and/or CTRL+D detected, forcing {0} to quit...".format(
                    self.PROGRAM_NAME), 1)
                return self.cleanup(1)

            except BaseException as error:
                self.latest_traceback = traceback.format_exc()
                printer.Printer().print_with_status("An unknown error occured:", 2)
                print(str(error))
                print(self.latest_traceback)
                return self.cleanup(10)

        else:
            self.logger.info("byebye is True, now quitting...")
            random_bye = ["Change your password regularly!",
                          "No Man-in-the-Middle!", "RSA and AES FTW!",
                          "Goodbye!", "WE NEED PRIVACY!",
                          "Use proxies!", "Maybe use Tor?",
                          "Pull requests available!", "Don't snoop on them!",
                          "Use secure communications!", "{0} made by EHVSN.".format(self.PROGRAM_NAME),
                          "We code this project overnight!",
                          "We are not doing anything illegal, right?",
                          "Don't be shy to make a pull request on https://github.com/ehvsn-team/Idle-Node.git !"]
            if random.randint(0, 100) > 70:
                random_bye = []

            print(quote.quote(random_bye))
            return self.cleanup(0)

# If running independently, run main() function.
if __name__ == '__main__':
    exit_code = 999
    try:
        i = 0
        args = {}
        abort_start = False
        help_menu = """\
--help | -h                                     Show this help menu and exit.

--no-gui | -g                                      Disable Graphical User Interface

--config-file=[FILEPATH] | -c [FILEPATH]        Use the configuration file <FILEPATH>.
--logfile=[FILEPATH] | -l [FILENAME]            Specify a path on where to write the logs.
--override-version-check                        Disable python version checking on startup.

--debug | -d                                    Enable debug mode.
--test | -t                                     Start test suite.
"""

        while i < len(sys.argv):
            if sys.argv[i].startswith(("--help", "-h")):
                print()
                print(help_menu)
                print()
                exit_code = 0
                abort_start = True
                break

            elif sys.argv[i].startswith(("--no-gui", "-g")):
                args['no-gui'] = False

            elif sys.argv[i].startswith("--config-file"):
                try:
                    configfile2use = sys.argv[i].partition('=')[2]
                    if os.path.exists(configfile2use):
                        if os.path.isfile(configfile2use):
                            args['configfile'] = configfile2use

                        else:
                            printer.Printer().print_with_status("Filepath is a directory!")
                            print()
                            print(help_menu)
                            print()
                            abort_start = True
                            break

                    else:
                        printer.Printer().print_with_status("Filepath does not exist!")
                        print()
                        print(help_menu)
                        print()
                        abort_start = True
                        break

                except IndexError:
                    printer.Printer().print_with_status("Please specify the configuration file path!", 2)
                    print()
                    print(help_menu)
                    print()
                    abort_start = True
                    break

            elif sys.argv[i].startswith("-c"):
                try:
                    i += 1
                    configfile2use = sys.argv[i]
                    if os.path.exists(configfile2use):
                        if os.path.isfile(configfile2use):
                            args['configfile'] = configfile2use

                        else:
                            printer.Printer().print_with_status("Filepath is a directory!")
                            print()
                            print(help_menu)
                            print()
                            abort_start = True
                            break

                    else:
                        printer.Printer().print_with_status("Filepath does not exist!")
                        print()
                        print(help_menu)
                        print()
                        abort_start = True
                        break

                except IndexError:
                    printer.Printer().print_with_status("Please specify the configuration file path!", 2)
                    print()
                    print(help_menu)
                    print()
                    abort_start = True
                    break

            elif sys.argv[i].startswith("--logfile"):
                try:
                    args['logfile'] = sys.argv[i].partition('=')[2]

                except IndexError:
                    printer.Printer().print_with_status("Please specify the logfile path!", 2)
                    print()
                    print(help_menu)
                    print()
                    abort_start = True
                    break

            elif sys.argv[i].startswith("-l"):
                try:
                    i += 1
                    args['logfile'] = sys.argv[i]

                except IndexError:
                    printer.Printer().print_with_status("Please specify the configuration file path!", 2)
                    print()
                    print(help_menu)
                    print()
                    abort_start = True
                    break

            elif sys.argv[i].startswith("--override-version-check"):
                args['override_pyvercheck'] = True

            elif sys.argv[i].startswith(("--debug", "-d")):
                args['debug_mode'] = True

            elif sys.argv[i].startswith(("--test", "-t")):
                printer.Printer().print_with_status("Not yet developed!", 1)
                abort_start = True
                break

            else:
                if sys.argv[i] == sys.argv[0]:
                    i += 1
                    continue

                print()
                print("[E] Unknown argument `{0}`!".format(sys.argv[i]))
                print()
                print(help_menu)
                print()
                exit_code = 13
                abort_start = True
                break

            i += 1

        del i
        if abort_start == False:
            if args.get('no-gui', False) == True:
                # Do not import Tkinter.
                pass

            else:
                try:
                    import tkinter

                except ImportError:
                    printer.Printer().print_with_status("An error occured while importing Tkinter module!", 2)
                    printer.Printer().print_with_status("Program will continue but GUI will be disabled.", 1)
                    print()
                    print("==================== TRACEBACK ====================")
                    traceback.print_exc()
                    print("===================================================")
                    print()
                    args['no-gui'] = True
                    time.sleep(3)

            # Call main method
            exit_code = MainClass(args).main()

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
