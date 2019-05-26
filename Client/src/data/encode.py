import os
import sys
import base64

# Encode config files.
def main():
    for filename in ["config.dat", "contact_list.lst", "real_config.dat"]:
        encode(filename)

def encode(filename):
    with open(filename, 'r') as f:
        encoded = base64.b64encode(f.read().encode())

    with open(filename, 'w') as f:
        f.write(str(encoded.decode()))

if __name__ == '__main__':
    main()
