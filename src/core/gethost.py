import socket
import sys
import os

def byname(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
 
    except socket.gaierror:
        err = "Invalid Domain or no internet connection."
        return err

def byaddr(ip):
    try:
        host = socket.gethostbyaddr(ip)
        return host

    except socket.herror:
        err = "Invalid IP Address or no internet connection."
        return err
