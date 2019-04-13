"""
Idle-Node Python Server
version 1.0
"""
# Coding=UTF-8

# Import directives
try:
    import os
    import sys
    import traceback

    import socket
    import select

except(ImportError, ModuleNotFoundError):
    print("[!] A module is missing! Please install the required modules...")
    print("==================== TRACEBACK ====================")
    traceback.print_exc()
    print("===================================================")
    sys.exit(1)

if __name__ == '__main__':
    main()