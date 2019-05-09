import os
import sys
import time

import signal
import socket

from core import multitasking
from core import logger

"""
comms_manager.py

Handles communications between peers and/or servers.
"""

# Kill all running tasks on CTRL+C.
signal.signal(signal.SIGINT, multitasking.killall)

class PeerToPeer(object):
    """
    class PeerToPeer():
        Creates a connection between two peers.

        :param remote_ip type(str): The peer's IP Address or domain name.
        :param connection_name type(str): The object name.

    Usage:

        from core import comms_manager

        new_connection = comms_manager.PeerToPeer("192.168.0.101", "ConnectionName")

        conn = new_connection

        conn.invite()
        conn.connect()

    """

    def __init__(self, remote_ip, connection_name=__name__, logger_obj=None):
        """
        def __init__(self):
            The initialization method of PeerToPeer() class.

        """

        self.name = connection_name
        self.creation_time = time.asctime()
        self.remote_ip = remote_ip

        if logger_obj is None:
            self.logger = logger.LoggingObject(name=__name__, logfile="data/comms.log")

        else:
            self.logger = logger_obj

    def invite(self):
        self.logger.info("Creating socket object...")
        socket_obj = socket.socket()
        self.logger.info("Trying to connect to peer...")
        socket_obj.connect((peer_address, 30000))

def ping(remote_ip):
    """
    def ping():
        Ping <remote_ip>.

    """

    socket_obj = socket.socket()
    socket_obj.connect((peer_address, 30000))
    socket_obj.sendall()

# @multitasking.task
def activate_redirection_port():
    """
    def activate_redirection_port():
        Listen for connection on port 30,000.

    """

    pass
    # DEV0003