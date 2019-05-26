#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SimpleLib.py -- Simple Library of Random Objects
Copyright(C) 2017-2019 :: Catayao56 <Catayao56@gmail.com>

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
I removed try/except blocks to let you do other things if an exception occurs.
"""

# Import system modules.
import os
import sys

import time
import base64
import random
import hashlib
import datetime
import platform
import subprocess

# NOTE: I leave this here to support programs that use older versions of SimpleLib.
if sys.platform == 'linux' or sys.platform == 'darwin':
    # Foreground colors
    CR = '\033[31m'        # red
    CG = '\033[32m'        # green
    CY = '\033[33m'        # yellow
    CB = '\033[34m'        # blue
    CGR = '\033[90m'       # gray

    # Misc colors
    CP = '\033[35m'        # purple
    CC = '\033[36m'        # cyan

    # Extended colors
    CLM = '\033[95m'       # light magenta
    CLB = '\033[94m'       # light blue
    CLG = '\033[92m'       # light green
    CLY = '\033[93m'       # light yellow
    CLR = '\033[91m'       # light red
    CLC = '\033[96m'       # light cyan
    CLGR = '\033[37m'      # light gray

    # Background colors
    BW = '\033[7m'         # white
    BR = '\033[41m'        # red
    BG = '\033[42m'        # green
    BY = '\033[43m'        # yellow
    BB = '\033[44m'        # blue
    BM = '\033[45m'        # magenta
    BC = '\033[46m'        # cyan
    BGR = '\033[100m'      # gray

    BLGR = '\033[2m'       # light gray
    BLR = '\033[101m'      # light red
    BLG = '\033[102m'      # light green
    BLY = '\033[103m'      # light yellow
    BLB = '\033[104m'      # light blue
    BLM = '\033[105m'      # light magenta
    BLC = '\033[106m'      # light cyan
    BLW = '\033[107m'      # light white?!?

    # Font types
    FB = '\033[1m'         # bold
    FI = '\033[3m'         # italic
    FU = '\033[4m'         # underline
    FE = '\033[9m'         # erased

    END = '\033[0m'        # reset to default...

else:
    # No color support on windows operating systems.
    CR = ''
    CG = ''
    CY = ''
    CB = ''
    CGR = ''

    CP = ''
    CC = ''
    CK = ''

    CLM = ''
    CLB = ''
    CLG = ''
    CLY = ''
    CLR = ''
    CLC = ''
    CLGR = ''

    BW = ''
    BR = ''
    BG = ''
    BY = ''
    BB = ''
    BM = ''
    BC = ''
    BGR = ''

    BLGR = ''
    BLR = ''
    BLG = ''
    BLY = ''
    BLB = ''
    BLM = ''
    BLC = ''
    BLW = ''

    FB = ''
    FI = ''
    FU = ''
    FE = ''

    END = ''

# Define Constants
global MODULE_NAME
global MODULE_HISTORY
global MODULE_VERSION
global COPYRIGHT
MODULE_NAME = "Simple Library"
MODULE_VERSION = 1.9
MODULE_HISTORY = {
    "1.10": "Added list_directory_tree()",
    "1.9": "get_python_version(), encode(), and decode() added",
    "1.8": "is_windows() variable `PLATFORM` is now lower-cased. \
    Updated captcha_picker(), now it is named captcha(). \
    Updated get_program_filename()",
    "1.7": "Colors are now in dictionaries.",
    "1.6": "Moved colors inside SimpleLib() class.",
    "1.5": "Added get_terminal_size(), set_terminal_size(), prsg(), \
    and word_chooser() on SimpleLib() class.",
    "1.4": "Added characters and wordlist variables in SimpleLib() class.",
    "1.3": "Added random_color() and captcha_picker().",
    "1.2": "Added get_program_filename().",
    "1.1": "Added proper_exit().",
    "1.0": "Added color variables, program_restart(), clrscrn(), pause(), \
    get_platform(), is_windows(), generate_session_id(), and hash().",
    "0.9": "Added path_exists(), isfile(), and isfolder().",
    "0.8": "Added pip_install().",
    "0.7": "Added geteuid().",
    "0.6": "Created a new module that uses a class.",
    "0.5": "Added ANSI code variables.",
    "0.4": "Added set_title().",
    "0.3": "Added freq_counter().",
    "0.2": "Added gethost() and logger().",
    "0.1": "First working version of SimpleLib."
}

COPYRIGHT = "Copyright(C) 2017-{0} by Catayao56".format(
        datetime.datetime.now().year)

class SimpleLib:
    """
    class SimpleLib():
        Class of miscellaneous methods.
    """

    def __init__(self):
        """
        def __init__():
            Initialization method of SimpleLib() class.
        """

        self.characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                           'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                           'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                           'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
                           'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                           'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V' ,'W', 'X',
                           'Y', 'Z', '!', '@', '#', '$', '%', '^', '&', '*',
                           '(', ')', '-', '_', '=', '+', '[', '{', ']', '}',
                           ';', ':', '\'', '"', '\\', '|', ',', '<', '.', '>',
                           '', '/', '?']

        self.wordlist = ["apple", "banana", "chair", "dog", "egg", "faith",
                         "grenade", "hopper", "igloo", "jackhammer", "kangaroo",
                         "lamp", "miniature", "natural", "opposite", "positive",
                         "quilt", "rain", "sun", "tanker", "umbrella", "vase",
                         "whale", "xylophone", "yellow", "zebra"]

        # Foreground colors (Does not work on Windows Systems!)
        foreground_colors = {
        "default": "\033[0m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "gray": "\033[90m",
        "grey": "\033[90m",  # I don't know what is the right spelling!
        # Extended colors
        "purple": "\033[35m",
        "violet": "\033[35m",
        "cyan": "\033[36m",
        # Light colors
        "light_gray": "\033[37m",
        "light_grey": "\033[37m",
        "light_red": "\033[91m",
        "light_green": "\033[92m",
        "light_yellow": "\033[93m",
        "light_blue": "\033[94m",
        "light_magenta": "\033[95m",
        "light_cyan": "\033[96m"
        }

        # Background colors (Does not work on Windows Systems!)
        background_colors = {
        "default": "\033[0m",
        "white": "\033[7m",
        "red": "\033[41m",
        "green": "\033[42m",
        "yellow": "\033[43m",
        "blue": "\033[44m",
        "magenta": "\033[45m",
        "cyan": "\033[46m",
        "gray": "\033[100m",
        "grey": "\033[100m",
        # Light colors (by the way, i do not recommend using light colors as backgrounds :p)
        "light_gray": "\033[2m",
        "light_grey": "\033[2m",
        "light_red": "\033[101m",
        "light_green": "\033[102m",
        "light_yellow": "\033[103m",
        "light_blue": "\033[104m",
        "light_magenta": "\033[105m",
        "light_cyan": "\033[106m",
        "light_white": "\033[107m"  # LIGHT WHITE?!? ARE YOU KIDDING!?
        }

        # Font types (Does not work on Windows Systems!)
        fonts = {
        "default": "\033[0m",
        "bold": "\033[1m",
        "italic": "\033[3m",
        "underlined": "\033[4m",
        "erased": "\033[9m"
        }

        # For captchas.
        captchas = [
        "Type this text.",
        "Please type this text.",
        "Don't type this text.",
        "Type this text now!",
        "Type this text to proceed."
        ]

    def program_restart(self):
        """
        def program_restart():
            Restart program.
        """

        sysexec = sys.executable
        os.execl(sysexec, sysexec, * sys.argv)

    def clrscrn(self, platform=None):
        """
        def clrscrn():
            Clears the screen.
        """

        if platform is None:
            platform = self.is_windows()

        if platform is False:
            subprocess.call('clear', shell=True)

        elif platform is True:
            subprocess.call('cls', shell=True)

        else:
            loop = 0
            while loop != 100:
                print()
                loop += 1

    def pause(self, info="Press enter to continue..."):
        """
        def pause():
            Wait for the user's input.
        """
        try:
            input(info)

        except(KeyboardInterrupt, EOFError):
            return 1

        finally:
            return 0

    def get_platform(self, mode=0):
        """
        def get_platform():
            Get the system platform.
        """

        if mode == 0:
            result = sys.platform
            """
            Possible Outputs:
            .---------------------.------------.
            | System              | Value      |
            |---------------------|------------|
            | Linux (2.x and 3.x) | linux2 (*) |
            | Windows             | win32      |
            | Windows/Cygwin      | cygwin     |
            | Mac OS X            | darwin     |
            | OS/2                | os2        |
            | OS/2 EMX            | os2emx     |
            | RiscOS              | riscos     |
            | AtheOS              | atheos     |
            | FreeBSD 7           | freebsd7   |
            | FreeBSD 8           | freebsd8   |
            | FreeBSD N           | freebsdN   |
            | OpenBSD 6           | openbsd6   |
            | ???                 | None       |
            '---------------------'------------'
            """

        elif mode == 1:
            result = os.name
            """
            Possible Outputs:
            .---------------------.------------.
            | System              | Value      |
            |---------------------|------------|
            | Windows, Cygwin     | nt         |
            | Linux, Mac OS X     | posix      |
            | Java                | java       |
            | ???                 | None       |
            '---------------------'------------'
            """

        elif mode == 2:
            result = platform.system()
            """
            Possible Outputs:
            .---------------------.------------.
            | System              | Value      |
            |---------------------|------------|
            | Windows, Cygwin     | Windows    |
            | Linux, Mac OS X     | Linux      |
            | Java                | Java       |
            | ???                 | None       |
            '---------------------'------------'
            """

        elif mode == 3:
            result = platform.uname()
            """
            Return a 5-tuple containing information identifying the current operating system.

            The tuple contains 5 strings:

            (sysname,
            nodename,
            release,
            version,
            machine)

            Some systems truncate the nodename to 8 characters or to the leading component;
            a better way to get the hostname is socket.gethostname() or even
            socket.gethostbyaddr(socket.gethostname()).
            """

        else:
            result = sys.platform

        return result

    def is_windows(self):
        """
        def is_windows():
            Check if system is windows.
        """
        platform = os.name
        if platform == 'nt':
            return True

        else:
            return False

    def generate_session_id(self):
        """
        def generate_session_id():
            Generate a session ID.
        """

        session = {}

        session['ID'] = random.randint(100000, 999999)
        session['ID_hash'] = self.hash(str(session['ID']), 'sha3_512')
        session['time_generated'] = time.strftime("%H:%M:%S :: %m/%d/%Y")
        return session

    def hash(self, string, hashtype='md5'):
        """
        def hash():
            Hashlib module wrapper.
        """

        string = string.encode()
        hashtype = hashtype.lower()
        if hashtype == 'blake2b':
            result = hashlib.blake2b(string).hexdigest()
            result = result.upper()
            return result

        elif hashtype == 'blake2s':
            result = hashlib.blake2s(string).hexdigest()
            result = result.upper()
            return result

        elif hashtype == 'sha3_224':
            result = hashlib.sha3_224(string).hexdigest()
            result = result.upper()
            return result

        elif hashtype == 'sha3_256':
            result = hashlib.sha3_256(string).hexdigest()
            result = result.upper()
            return result

        elif hashtype == 'sha3_384':
            result = hashlib.sha3_384(string).hexdigest()
            result = result.upper()
            return result

        elif hashtype == 'sha3_512':
            result = hashlib.sha3_512(string).hexdigest()
            result = result.upper()
            return result

        elif hashtype == 'shake_128':
            result = hashlib.shake_128(string).hexdigest()
            result = result.upper()
            return result

        elif hashtype == 'shake_256':
            result = hashlib.shake_256(string).hexdigest()
            result = result.upper()
            return result

        elif hashtype == 'md5':
            result = hashlib.md5(string).hexdigest()
            result = result.upper()
            return result

        elif hashtype == 'sha1':
            result = hashlib.sha1(string).hexdigest()
            result = result.upper()
            return result

        elif hashtype == 'sha224':
            result = hashlib.sha224(string).hexdigest()
            result = result.upper()
            return result

        elif hashtype == 'sha256':
            result = hashlib.sha256(string).hexdigest()
            result = result.upper()
            return result

        elif hashtype == 'sha384':
            result = hashlib.sha384(string).hexdigest()
            result = result.upper()
            return result

        elif hashtype == 'sha512':
            result = hashlib.sha512(string).hexdigest()
            result = result.upper()
            return result

        else:
            raise ValueError("An unknown hash type is entered.")

    def path_exists(self, file_path):
        """
        def path_exists():
            Return True if path exists.
        """

        return os.path.exists(file_path)

    def isfile(self, file_path):
        """
        def isfile():
            Return True if path is a file.
        """

        return os.path.isfile(file_path)

    def isfolder(self, file_path):
        """
        def isfolder():
            Return True if path is a directory.
        """

        return os.path.isdir(file_path)

    def pip_install(self, package, pyver):
        """
        def pip_install():
            Install a module using PIP.
        """

        if pyver == 3:
            subprocess.Popen(args='pip3 install ' + package,
                    shell=True, universal_newlines=True)

        elif pyver == 2:
            subprocess.Popen(args='pip2 install ' + package,
                    shell=True, universal_newlines=True)

        else:
            subprocess.Popen(args='pip install ' + package,
                    shell=True, universal_newlines=True)

    def geteuid(self):
        """
        def geteuid():
            Return the current process's effective user id.
        """

        try:
            euid = os.geteuid()

        except Exception:
            # Might be running on windows...
            euid = 0

        return euid

    def random_color(self, color_list=[]):
        """
        def random_color():
            Return a random color.
        """

        if color_list == []:
            for color in self.foreground_colors:
                color_list.append(self.foreground_colors[color])

        randomizer = random.randint(0, (len(color_list) - 1))
        return color_list[randomizer]

    def captcha(self, mode=0, **kwargs):
        """
        def captcha_picker():
            Check if user is not a robot.

            mode (int): 0 == Enter the string.
                        1 == Solve the math problem.
                        2 == Unscramble the word.

            **kwargs (dict):
                Values available in all modes:
                    prompt (str): Do you want to use a custom prompt?

                Mode #0 (Enter the string):
                    captcha_list (list): A list of captchas to use.
                    case_sensitive (bool): Is the user need to enter the exact character?

                Mode #1 (Solve the math problem):
                    difficulty (int): Set difficulty. (0~1)
                    operations (list): A list of operations to use ('+', '-', '*', or '/')

                Mode #2 (Unscramble the word):
                    wordlist (list): A list of words to be scrambled.
        """

        if mode == 0:
            try:
                captcha_list = list(kwargs["captcha_list"])

            except(KeyError, ValueError, TypeError):
                captcha_list = self.captchas

            try:
                prompt = str(kwargs["prompt"])

            except(KeyError, ValueError, TypeError):
                prompt = " >>> "

            try:
                case_sensitive = bool(kwargs["case_sensitive"])

            except(KeyError, ValueError, TypeError):
                case_sensitive = False

            random_captcha = captcha_list[random.randint(0, (len(captcha_list) - 1))]

            if ' ' in random_captcha:
                print("Please enter the sentence below:")

            else:
                print("Please enter the character/s below:")

            print("\n{0}\n".format(random_captcha))
            verification = input(prompt)
            if case_sensitive is False:
                if verification.lower() == random_captcha.lower():
                    return 0

                else:
                    return 1

            else:
                if verification == random_captcha:
                    return 0

                else:
                    return 1

        elif mode == 1:
            try:
                difficulty = int(kwargs["difficulty"])

            except(KeyError, ValueError, TypeError):
                difficulty = random.randint(0, 1)

            try:
                try:
                    operations = list(kwargs["operations"])

                except(TypeError, ValueError):
                    operations = tuple(kwargs["operations"])

                for operation in operations:
                    if operation not in ["+", "-", "*", "/"]:
                        raise ValueError("Operation list must have `+`, `-`, `*`, and/or `/` only!")

            except(KeyError, ValueError, TypeError):
                operations = ['+', '-', '*', '/']

            try:
                prompt = str(kwargs["prompt"])

            except(KeyError, ValueError, TypeError):
                prompt = " >>> "

            if difficulty < 0 or difficulty > 5:
                raise ValueError("difficulty must be 0~5!")

            else:
                if difficulty == 0:
                    operation_to_use = "/"
                    if len(operations) == 1 and "/" in operations:
                        pass

                    else:
                        while operation_to_use == "/":
                            operation_to_use = operations[random.randint(0, (len(operations) - 1))]

                    number = []
                    number.append(random.randint(0, 100))
                    number.append(random.randint(0, 100))
                    print("Solve the following to continue:")
                    print("\n{0} {1} {2} = ???\n".format(str(number[0]), operation_to_use, str(number[1])))
                    verification = input(prompt)
                    if operation_to_use == "+":
                        if str(number[0] + number[1]) == verification:
                            return 0

                        else:
                            return 1

                    elif operation_to_use == "-":
                        if str(number[0] - number[1]) == verification:
                            return 0

                        else:
                            return 1

                    elif operation_to_use == "*":
                        if str(number[0] * number[1]) == verification:
                            return 0

                        else:
                            return 1

                    elif operation_to_use == "/":
                        if str(number[0] / number[1]) == verification:
                            return 0

                        else:
                            return 1

                elif difficulty == 1:
                    operation1 = operations[random.randint(0, (len(operations) - 1))]
                    operation2 = "/"
                    if len(operations) == 1 and "/" in operations:
                        pass

                    else:
                        while operation2 == "/":
                            operation2 = operations[random.randint(0, (len(operations) - 1))]

                    number = []
                    number.append(random.randint(1, 100))
                    number.append(random.randint(1, 50))
                    number.append(random.randint(2, 4))
                    print("Solve the following to continue:")
                    print("\n{0} {1} {2} = n {3} {4} = ???\n".format(str(number[0]), operation1, str(number[1]), operation2, str(number[2])))
                    verification = input(prompt)
                    if operation1 ==  "+":
                        res = number[0] + number[1]

                    elif operation1 == "-":
                        res = number[0] - number[1]

                    elif operation1 == "*":
                        res = number[0] * number[1]

                    elif operation1 == "/":
                        res = number[0] / number[1]

                    if operation2 == "+":
                        if str(res + number[2]) == verification:
                            return 0

                        else:
                            return 1

                    elif operation2 == "-":
                        if str(res + number[2]) == verification:
                            return 0

                        else:
                            return 1

                    elif operation2 == "*":
                        if str(res + number[2]) == verification:
                            return 0

                        else:
                            return 1

                    elif operation2 == "/":
                        if str(res + number[2]) == verification:
                            return 0

                        else:
                            return 1

        elif mode == 2:
            try:
                try:
                    wordlist = list(kwargs["wordlist"])

                except(TypeError, ValueError):
                    wordlist = tuple(kwargs["wordlist"])

            except(KeyError, ValueError, TypeError):
                wordlist = self.wordlist

            try:
                prompt = str(kwargs["prompt"])

            except(KeyError, ValueError, TypeError):
                prompt = " >>> "

            word = str(wordlist[random.randint(0, (len(wordlist) - 1))])
            if len(word) < 2 or len(word) > 30:
                raise ValueError("Word length must be 0~30 characters only!")

            else:
                if len(word) == 2:
                    captcha = word[1] + word[0]

                elif len(word) == 3:
                    captcha = word[0] + word[2] + word[1]

                elif len(word) == 4:
                    captcha = word[2] + word[3] + word[0] + word[1]

                elif len(word) == 5:
                    captcha = word[3] + word[4] + word[0] + word[1] + word[2]

                else:
                    if type(len(word) / 2) == int:
                        captcha = ""
                        i = (len(word) / 2) - 1
                        while i <= (len(word) - 1):
                            i += 1
                            captcha += word[i]

                        i = 0
                        while i < (len(word)):
                            captcha += word[i]
                            i += 1

                    else:
                        captcha = word[::-1]

                captcha = captcha.lower()
                print("Please unscramble the following to continue:")
                print("\n{0}\n".format(captcha))
                verification = input(prompt)
                if word.lower() == verification:
                    return 0

                else:
                    return 1

        else:
            raise ValueError("Unknown mode!")

    def get_program_filename(self, current_path=None):
        """
        def get_program_filename():
            Get the program's filename.
        """

        if current_path is None:
            current_path = sys.argv[0]

        separator = os.sep
        current_path = current_path[::-1]
        filename = current_path.partition(separator)[0]
        filename = filename[::-1]
        return filename

    def proper_exit(self, exit_code=random.randint(0, 999999)):
        """
        def proper_exit():
            Exit the program gracefully.
        """

        try:
            sys.exit(exit_code)

        except SystemExit:
            os._exit(exit_code)

    def get_terminal_size(self):
        """
        def get_terminal_size():
            Get the terminal size.
        """

        # DEV0001: NOT YET TESTED!
        result = shutil.get_terminal_size()
        return result

    def set_terminal_size(self, lines, columns):
        """
        def set_terminal_size():
            Set the terminal size.
        """

        # DEV0001: NOT YET TESTED!
        if os.name == 'nt':
            return os.system("mode con: cols={0} lines={1}".format(columns, lines))

        # DEV0004: Continue this!
        elif sys.platform.startswith("linux"):
            pass

        else:
            pass

    def prsg(self, length=20, characters=[]):
        """
        def prsg():
            Pseudo Random String Generator
        """

        if characters == []:
            characters = self.characters

        result = ""
        i = 0
        while i < length:
            i += 1
            result += characters[random.randint(0, (len(characters) - 1))]

        return result

    def word_chooser(self, words_to_pick=1, list_or_wordlist=[]):
        """
        def word_chooser():
            Choose a random word in the list or wordlist provided.
        """

        if list_or_wordlist == []:
            wordlist = self.wordlist

        if type(list_or_wordlist) is list:
            pass

        elif type(list_or_wordlist) is str:
            with open(list_or_wordlist, 'r') as f:
                wordlist = f.read().split('\n')

        else:
            raise TypeError("list_or_wordlist must be a word list or wordlist filename!")

        return wordlist[random.randint(0, (len(wordlist) - 1))]

    def encode(self, data, code="base64"):
        """
        def encode():
            Encode data in a number of ways.
        """

        if code.lower() == "base64":
            return base64.b64encode(data.encode()).decode()

        else:
            raise ValueError("Invalid code option!")

    def decode(self, data, code="base64"):
        """
        def decode():
            Decode data in a number of ways.
        """

        if code.lower() == "base64":
            return base64.b64decode(data.encode()).decode()

        else:
            raise ValueError("Invalid code option!")

    def get_python_version(self):
        """
        def get_python_version():
            Get the interpreter version of Python.
        """

        ver = sys.version_info
        return "{0}.{1}.{2}".format(ver[0], ver[1], ver[2])

    def seconds_to_datetime(self, seconds, format="%A, %B %d, %Y %I:%M:%S"):
        """
        def seconds_to_datetime():
            Convert seconds to human-readable date and time.

        """

        return datetime.fromtimestamp(seconds).strftime(format)

    def seconds_to_hms(self, seconds):
        """
        def seconds_to_hms():
            Convert seconds to human-readable Hours, Minutes, and Seconds.

        """

        return datetime.timedelta(seconds=seconds)

    def list_directory_tree(self, path=".", exceptions=[]):
        """
        def list_directory_tree():
            Return a list of directory paths. Recurse through subdirectories.

        """

        dirs = []
        filenames = []

        for dirname, dirnames, filenames in os.walk(path):
            for subdirname in dirnames:
                dirs.append(os.path.join(dirname, subdirname))

            for filename in filenames:
                filenames.append(os.path.join(dirname, filename))

            for exc in exceptions:
                if exc in dirnames:
                    dirnames.remove(exc)

        return dirs, filenames