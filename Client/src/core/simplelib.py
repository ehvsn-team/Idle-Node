#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SimpleLib.py -- Simple Library of random objects
Copyright(C) 2018 :: Catayao56 <Catayao56@gmail.com>

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# Import system modules.
import os
import sys

import time
import random
import hashlib
import datetime
import platform
import subprocess

# Define Constants
MODULE_NAME = "Simple Library"
MODULE_VERSION = 1.4

COPYRIGHT = "Copyright(C) 2017-{0} by Catayao56".format(
        datetime.datetime.now().year)

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

        pass

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
            pass

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
        PLATFORM = os.name
        if PLATFORM == 'nt':
            return True

        else:
            return False

    def generate_session_id(self):
        """
        def generate_session_id():
            Generate a session ID.
        """

        session = {}

        session['ID'] = random.randint(111111, 999999)
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

    def random_color(self):
        """
        def random_color():
            Return a random color.
        """

        color_list = [CR, CG, CY, CB, CGR, CP, CC, CLM, CLB, CLG, CLY,
                CLR, CLC, CLGR]
        randomizer = random.randint(0, (len(color_list) - 1))
        return color_list[randomizer]

    def captcha_picker(self, list_of_strings=[]):
        """
        def captcha_picker():
            Return random captchas.
        """

        if list_of_strings == []:
            list_of_strings = [
                    "Type this text.",
                    "Please type this text.",
                    "Don't type this text.",
                    "Type this text now!"
                    ]

        randomizer = random.randint(0, (len(list_of_strings)-1))
        return list_of_strings[randomizer]

    def get_program_filename(self, current_path):
        """
        def get_program_filename():
            Get the program's filename.
        """

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
