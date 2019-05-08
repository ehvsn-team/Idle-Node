#!/usr/bin/env python3

import os
import sys
import time
import random
import subprocess

try:
    import virtualenv
    
except ImportError, ModuleNotFoundError:
    print("[i] Cannot import virtualenv! please install it first.")
    sys.exit(3)

class main:
    """
    class main():
        The main class of CImulator.
    """

    def __init__(self):
        """
        def __init__():
            The initialization method of CImulator class.
        """

        # Program information
        self.name = "CI Emulator"
        self.version = "0.0.0.3"
        self.desc = "The simple alternative tool for auto DevOps."
        self.filename = sys.argv[0]
        self.banner = """   __________                __      __
  / ____/  _/___ ___  __  __/ /___ _/ /_____  _____
 / /    / // __ `__ \/ / / / / __ `/ __/ __ \/ ___/
/ /____/ // / / / / / /_/ / / /_/ / /_/ /_/ / /
\____/___/_/ /_/ /_/\__,_/_/\__,_/\__/\____/_/ v{0}
        "{1}" """.format(self.version, self.desc)

    def main(self):
        """
        def main():
            The main method of CImulator class.
        """

        misc().clrscrn()  # Clear the screen.

        # Check if git is installed.
        if ProjectManager().getGitExecutable() is False:
            print("[i] git is not found! Please install git first before proceeding.")
            sys.exit(3)

        # Check if directory has git project directory.
        if ProjectManager().getProjectName() is None:
            print("[i] git project directory wasn't found...\nDo you want me to initialize a new repository or abort this program?")
            print()
            print("[01] Create new git project.")
            print("[02] Abort startup.")
            while True:
                try:
                    ask = input(" >>> ")
                    if int(ask) == 1:
                        # Initialize git repository and restart.
                        if subprocess.getstatusoutput('git init')[0] == 0:
                            if os.name == "nt":
                                print("[i] Please restart {0} to continue...".format(self.name))
                                sys.exit(0)

                            else:
                                python = sys.executable
                                os.execl(python, python, * sys.argv)

                        else:
                            print("[i] Cannot create git project directory...\nPlease manually perform `git init` manually on this directory.")
                            sys.exit(2)

                    elif int(ask) == 2:
                        sys.exit(1)

                    else:
                        continue

                except(KeyboardInterrupt, EOFError, ValueError, TypeError):
                    continue

        # Check if repository is modified by CImulator.
        if ProjectManager().getCimulatorData() is False:
            try:
                os.mkdir('.CImulator')
                os.mkdir('.CImulator/development')
                with open('.CImulator/info', 'w') as f:
                    while True:
                        try:
                            project_name = input("Project Name: ")
                            project_desc = input("Project Description: ")

                        except(KeyboardInterrupt, EOFError):
                            continue

                        else:
                            result = """NAME :: {0}
DESCRIPTION :: {1}
CREATED :: {2}""".format(project_name, project_desc,
        time.strftime('%a, %I:%M %p %b. %d, %Y'))
                            f.write(result)
                            break

                with open('.git/info/exclude', 'a') as f:
                    f.write('\n.CImulator/\nCImulator.py\n')

                with open('.CImulator/development/taskboard', 'w') as f:
                    f.write("")
                    
                with open(".CImulator/development/phase", 'w') as f:
                    f.write("Undefined\n")

            except(IOError, EOFError, FileNotFoundError, PermissionError):
                print("[i] Cannot create CImulator data!")
                sys.exit(4)

            else:
                pass

        while True:
            try:
                misc().clrscrn()
                print()
                print(self.banner)
                print()
                print("Current project: {0}".format(str(ProjectManager().getProjectName())))
                print("Development Phase: {0}".format(ProjectManager().getProjectPhase()))
                print()
                print("Project Remote/s:")
                print(ProjectManager().getProjectRemotes())
                print()
                print("Git Commands")
                print("[01] Use binary search to find the commit that introduced a bug.")
                print("[02] Show commit log.")
                print("[03] Show project status.")
                print()
                print("Auto DevOps")
                print("[04] Task Board")
                print("[05] Progress Chart")
                print("[06] Perform test routine")
                print()
                print("[99] Quit")
                print()
                option = int(input(' >>> '))
                if option == 1:
                    ProjectManager().bisect()

                elif option == 2:
                    ProjectManager().commit_log(True)
                    input("Press enter to continue...")

                elif option == 3:
                    ProjectManager().status()
                    input("Press enter to continue...")

                elif option == 4:
                    AutoDevOps().taskboard_manager()

                elif option == 99:
                    sys.exit(0)

                else:
                    continue

            except(ValueError, TypeError, KeyboardInterrupt, EOFError):
                continue


class misc:
    """
    class misc():
        Miscellaneous methods.
    """

    def __init__(self):
        """
        def __init__():
            Initialization method for misc() class.
        """

        pass

    def clrscrn(self):
        """
        def clrscrn():
            Clear the contents of the screen.
        """

        if os.name == 'nt':
            subprocess.call(['cls'], shell=True)

        else:
            subprocess.call(['clear'], shell=True)

        return 0

    def commitNumberShortener(self, commit):
        """
        def commitNumberShortener():
            Shortens the commit number into a 6 hexadecimal characters.
        """

        result = ""
        i = 0
        while i < 6:
            try:
                result += commit[i]

            except IndexError:
                pass

            finally:
                i += 1

        return result
    
    def create_virtualenv(self, name):
        """
        def create_virtualenv():
            Create a new virtual environment.
        """

        if "|" in venv_path or "&" in venv_path or ";" in venv_path:
            return 2
        
        if os.system("virtualenv {0}".format(venv_path)) == 0:
            return 0
        
        else:
            return 1

    
    def activate_virtualenv(self, venv_path):
        """
        def activate_virtualenv():
            Activate the virtual environment <venv>.
        """
        
        if "|" in venv_path or "&" in venv_path or ";" in venv_path:
            return 2
        
        if os.system("source {0}".format(venv_path)) == 0:
            return 0
        
        else:
            return 1
        
    def deactivate_virtualenv(self):
        """
        def deactivate_virtualenv():
            Deactivate currently active virtual environment.
        """
        
        if os.system("deactivate") == 0:
            return 0
        
        else:
            return 1

class ProjectManager:
    """
    class ProjectManager():
        The main `processor` of CImulator.
    """

    def __init__(self):
        """
        def __init__():
            Initialization method of ProjectManager() class.
        """

        pass

    def getProjectName(self):
        """
        def getProjectName():
            Get the project name by two ways:
                + Based on what is the information given by user to CImulator.
                + Based on current directory with git.
        """

        try:
            with open('.CImulator/info', 'r') as f:
                name = f.readlines()
                name = name[0].partition(' :: ')[2]
                return name

        except(IOError, FileNotFoundError, EOFError, PermissionError, IndexError):
            files = os.listdir()
            if '.git' in files:
                name = os.getcwd()
                name = name[::-1]
                name = name.partition(os.sep)[0]
                name = name[::-1]
                return name

            else:
                return None

    def getProjectPhase(self):
        """
        def getProjectPhase():
            Get the current development phase of the project.
        """

        if self.getCimulatorData() is True:
            try:
                with open('.CImulator/development/phase', 'r') as f:
                    data = f.readline()

            except(IOError, EOFError, FileNotFoundError, PermissionError):
                return None

            else:
                return data

    def getProjectRemotes(self):
        """
        def getProjectRemotes():
            Get the project remotes.
        """

        try:
            result = subprocess.getstatusoutput('git remote -v')
            if result[0] == 0:
                return result[1]

            else:
                print("[i] An error occured with git!")
                return "AN ERROR OCCURED WITH GIT"

        except PermissionError:
            print("[i] An error occured with git!")
            return "AN ERROR OCCURED WITH GIT"

    def getGitExecutable(self):
        """
        def getGitExecutable():
            Check if git is installed on system.
        """

        if os.name == "nt":
            if subprocess.getstatusoutput("git help")[0] == 0:
                return True

            else:
                return False

        else:
            if subprocess.getstatusoutput("which git")[0] == 0:
                return True

            else:
                return False

    def getCimulatorData(self):
        """
        def getCimulatorData():
            Check if project has already been modified by Cimulator.
        """

        if os.path.isdir('.CImulator'):
            return True

        else:
            return False

    def getCommitNumber(self):
        """
        def getCommitNumber():
            Get the commit hash of the current commit.
        """

        try:
            data = subprocess.getstatusoutput("git show")
            if data[0] == 0:
                commit_number = data[1].partition(' ')[2]
                commit_number = commit_number.partition('\n')[0]
                scommit_number = misc().commitNumberShortener(commit_number)

            else:
                commit_number = "[ERROR WHILE FETCHING INFO]"
                scommit_number = "[ERROR WHILE FETCHING INFO]"

        except(PermissionError):
            print("[i] An error occured with git!")
            return 1

        else:
            return((commit_number, scommit_number))

    def bisect(self):
        """
        def bisect():
            Use binary search to find the commit that introduced a bug.
        """

        if subprocess.getstatusoutput('git bisect start')[0] == 0:
            pass

        else:
            print("[i] Cannot start bisection!")
            input("Press enter to continue...")
            return 1

        while True:
            try:
                misc().clrscrn()
                print()
                print(main().banner)
                print()
                commit = self.getCommitNumber()
                print("Commit {0} ( {1} )".format(commit[0], commit[1]))
                print()
                print("[01] Show status.")
                print("[02] Show changes on this commit.")
                print("[03] Test the commit.")
                print()
                print("[04] Mark {0} as a bad commit.".format(commit[1]))
                print("[05] Mark {0} as a good commit.".format(commit[1]))
                print()
                print("[99] End bisection.")
                print()
                option = int(input(' >>> '))
                if option == 1:
                    result = subprocess.getstatusoutput('git status')
                    if result[0] == 0:
                        misc().clrscrn()
                        print("Commit {0} ( {1} )".format(commit[0], commit[1]))
                        print()
                        print(result[1])
                        input("Press enter to continue...")
                        continue

                    else:
                        print("[i] An error occured with git!")
                        return 2

                elif option == 2:
                    result = subprocess.getstatusoutput('git diff')
                    if result[0] == 0:
                        misc().clrscrn()
                        print("Commit {0} ( {1} )".format(commit[0], commit [1]))
                        print()
                        print(result[1])
                        input("Press enter to continue...")
                        continue

                elif option == 3:
                    self.test_routine()

                elif option == 4:
                    out1 = subprocess.getstatusoutput('git bisect bad')
                    out2 = subprocess.getstatusoutput('git bisect next')
                    out = out1[0] + out2[0]
                    if out == 0:
                        print("[i] {0} is marked as bad.".format(commit[1]))
                        input("Press enter to continue...")

                    else:
                        print("[i] Cannot mark {0} as bad!".format(commit[1]))
                        print(out1[1], '\n', out2[1])
                        input("Press enter to continue...")

                elif option == 5:
                    out1 = subprocess.getstatusoutput('git bisect good')
                    out2 = subprocess.getstatusoutput('git bisect next')
                    out = out1[0] + out2[0]
                    if out == 0:
                        print("[i] {0} is marked as good.".format(commit[1]))
                        input("Press enter to continue...")

                    else:
                        print("[i] Cannot mark {0} as good!".format(commit[1]))
                        print(out1[1], '\n', out2[1])
                        input("Press enter to continue...")

                elif option == 99:
                    if subprocess.getstatusoutput('git bisect reset')[0] !=  0:
                        print("[i] Cannot end bisection! Please manually enter 'git bisect reset' in your terminal.")
                        input("Press enter to continue...")
                    return 0

                else:
                    continue

            except(ValueError, TypeError, KeyboardInterrupt, EOFError):
                continue
            
    def test_routine(self):
        """
        def test_routine():
            Perform test routine.
        """
        
        try:
            CImulator_temp = "CImulator{0}".format(random.randint(0, 1000))
            misc().create_virtualenv(CImulator_temp)
            if os.name == "nt":
                if os.system("%HOMEPATH%/{0}/Scripts/activate".format(CImulator_temp)) == 0:
                    pass
                
                else:
                    print("[i] Cannot activate virtual environment!")
                    return 1
                
            else:
                # DEV0003
        
        except:
            pass

    def commit_log(self, interactive=False):
        """
        def commit_log():
            Show the commit log.
        """

        if interactive is False:
            result = subprocess.getstatusoutput('git log --decorate=full --graph')
            if result[0] == 0:
                print(result[1])
                return 0
    
            else:
                print("[ERROR WITH GIT]")
                return 1
            
        else:
            result = os.system('git log --decorate=full --graph')
            if result == 0:
                return 0
    
            else:
                print("[ERROR WITH GIT]")
                return 1
            

    def status(self):
        """
        def status():
            Show project status.
        """

        # Get git status information.
        stats = subprocess.getstatusoutput('git status --show-stash')
        # Get CImulator information.
        project_name = self.getProjectName()
        try:
            with open('.CImulator/info', 'r') as f:
                data = f.readlines()
                description = data[1].partition(' :: ')[2]
                creation_date = data[2].partition(' :: ')[2]

        except(IOError, FileNotFoundError, EOFError, PermissionError, IndexError):
            pass

        # Check if something is wrong.
        if stats[0] != 0:
            print("[i] There is a problem with git!")
            return 1

        elif project_name == None:
            print("[i] Cannot get project name!")
            return 2

        else:
            misc().clrscrn()
            print()
            print(main().banner)
            print()
            print("Project Name: {0}".format(project_name))
            print("\t{0}".format(description))
            print()
            print("Creation Date: {0}".format(creation_date))
            print("Project Phase: {0}".format(self.getProjectPhase()))
            print("\nProject Remotes:\n{0}".format(self.getProjectRemotes()))
            print()
            print("Latest commit: {0}".format(self.getCommitNumber()[1]))
            print()
            return 0

class AutoDevOps(object):
    """
    class AutoDevOps():
        Class for managing auto DevOps.
    """

    """
    DEV0003:
    task board, phases, etc.
    """

    def __init__(self):
        pass

    def taskboardmanager(self):
        while True:
            try:
                misc().clrscrn()
                print()
                print(main().banner)
                print()
                commit = self.getCommitNumber()
                print("Commit {0} ( {1} )".format(commit[0], commit[1]))
                print()
                print("[01] Show tasks.")
                print("[02] Add new task")
                print("[03] Update task")
                print("[04] Remove task")
                print()
                print("[99] Back to main menu")
                print()
                option = int(input(" >>> "))
                if option == 1:
                    misc().clrscrn()
                    try:
                        with open(".CImulator/development/taskboard", 'r') as f:
                            tasks = f.readlines()

                        if len(tasks) != 0:
                            for task in tasks:
                                tsk = task.split(":;:split:;:")
                                print("========================================")
                                print("Task Number: {0}".format(tsk[0]))
                                print("Task: {0}".format(tsk[1]))
                                print("Description:\n{0}".format(tsk[2]))
                                print()
                                
                        else:
                            print("[i] No tasks yet!")

                    except(FileNotFoundError, EOFError, PermissionError, IOError):
                        print("[E] Cannot list tasks!")
                        input("Press enter to continue...")

                    else:
                        input("Press enter to continue...")

                elif option == 2:
                    pass
                    # DEV0003: Continue this

                elif option == 99:
                    return 0

                else:
                    continue

            except(ValueError, TypeError, KeyboardInterrupt, EOFError):
                continue

if __name__ == '__main__':
    main().main()
