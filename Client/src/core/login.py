#!/usr/bin/env python
#-*- coding: utf-8 -*-

try:
    import os
    import sys
    import traceback
    import hashlib
    from getpass import getpass

except ImportError:
    print('Error importing modules!')
    traceback.print_exc()
    sys.exit(0)

def try_open(udata):
    udata = str(udata)
    try:
        open(udata, 'r').read()
        open(udata, 'r').close()

    except:
        open(udata, 'w').write('')
        open(udata, 'w').close()

def login(udata):
    udata = str(udata)
    try_open(udata)
    n = 0
    Name = str(input("Username: "))
    D_Name = Name
    Name = Name.encode()
    Crypt_Name_Log = hashlib.sha1(Name).hexdigest()
    with open(udata, 'r') as f:
        data = f.read()
        if Crypt_Name_Log not in data:
            print('Unknown User, try again !')
            f.close()
            return None

        else:
            Password = getpass().encode()
            Crypt_Pass_Log = hashlib.sha1(Password).hexdigest()
            string_name_password = Crypt_Name_Log + ' : ' + Crypt_Pass_Log
            if string_name_password in data:
                print('Welcome', D_Name, '! You\'re logged in!')
                f.close()
                for char in Password:
                    n += 1

                Password_Hidden = n*'*'
                login_valid(D_Name, Password_Hidden)
                return D_Name

            else:
                print('An error occured, please check the Password.')
                f.close()
                return None

def login_valid(D_Name, Password_Hidden):
    print('Profile : ', '\n', 'Name : ', D_Name, '\n', 'Password : ', Password_Hidden)

def register(udata):
    udata = str(udata)
    try_open(udata)
    while True:
        Name = str(input("Username: "))
        if Name == "" or Name == None:
            print("Invalid Username!")
            continue

        else:
            break

    Name = Name.encode()
    Crypted_Name = hashlib.sha1(Name).hexdigest()
    with open(udata, 'r') as f:
        data = f.read()
        if Crypted_Name in data:
            print('This Name is already used by another person, please choose another one!')
            f.close()

        else:
            Password = getpass()
            Confirm_Password = getpass('Confirm the password: ')
            with open(udata, 'a') as t:
                if Password == Confirm_Password:
                    Password = Password.encode()
                    Crypted_Password = hashlib.sha1(Password).hexdigest()
                    t.write(Crypted_Name)
                    t.write(' : ')
                    t.write(Crypted_Password)
                    t.write('\n')
                    t.close()
                    print('Account created! You can now login!')
                    f.close()

                else:
                    print('Error, the two passwords don\'t match!')
                    t.close()
