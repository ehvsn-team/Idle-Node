<<<<<<< HEAD
# -*- coding: utf-8 -*-

import sys
import os
import socket


def current():
    """
    def current():
        return the current hostname
    """

    try:
        hostname = socket.gethostname()

    except Exception as error:
        return error

    else:
        return hostname


def byname(domain):
    """
    def byname():
        map a hostname to its IP number

        :param domain: Domain to map.
        :type str:

        :returns: ip or error exception
        :return type: str <specific>Exception
    """

    try:
        ip = socket.gethostbyname(domain)
        return ip

    except Exception as error:
        return error

    else:
        return ip


def byaddr(ip):
    """
    def byaddr():
        map an IP number or hostname to DNS info

        :param ip: IP to map.
        :type str:

        :returns: ip or Exception
        :return type: str or <specific>Exception
    """

    try:
        host = socket.gethostbyaddr(ip)

    except Exception as error:
        return error

    else:
        return host
