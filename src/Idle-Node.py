#!/usr/bin/env python

# Import directives
try:
    import os
    import sys
    import time
    import traceback

except ImportError:
    # Prints if error is encountered while importing modules.
    print("Import Error!")
    print()
    print("==================== TRACEBACK ====================")
    traceback.print_exc()
    print("===================================================")
    sys.exit(1)

def main(): # The Main Function
    print("Hello, world!") # Prints Hello, world! in the screen.
    time.sleep(3)
    input("Press enter to continue...")
    return 0 # Returns 0...

# If running independently, run main() function.
if __name__ == '__main__':
    exit_code = main()
    try:
        sys.exit(exit_code)

    except SystemExit:
        os._exit(exit_code)
        