import os
import sys

import base64

# Decode config files.
def main():
    for filename in ["config.dat", "contact_list.lst"]:
        encode(filename)
        
def encode(filename):
    with open(filename, 'r') as f:
        decoded = base64.b64decode(f.read())
        
    with open(filename, 'w') as f:
        f.write(str(decoded.decode()))

if __name__ == '__main__':
    main()