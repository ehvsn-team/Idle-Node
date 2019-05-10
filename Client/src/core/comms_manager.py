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

class Main(object):
    """
    class Main():
        The default class of comms_manager.py module.
        
        :param connection_name type(str): The object name.
        
        :param logger_obj type(object): The logger instance.
        :param socket_type type(str): The socket type (`TCP` or `UDP`)
        :param protocol_family type(str): The address/protocol family (`IPV4` or `IPV6`)

    Usage:

        from core import comms_manager

        new_connection = comms_manager.Main("ConnectionName")

        conn = new_connection

        conn.activate_redirection_port(30000)
        
        conn.close()

    """

    def __init__(self, connection_name=__name__, logger_obj=None, **kwargs):
        """
        def __init__(self):
            The initialization method of Main() class.

        """

        self.name = connection_name
        self.creation_time = time.asctime()
        self.broadcast_ip = "0.0.0.0"
        self.port = 30000
        
        # Contains: <ip>: <port> <last connection>
        # last connection is for limiting ip connection.
        self.connections = {}
        self.max_backlog = 10
        
        self.kill_signal = False

        if logger_obj is None:
            self.logger = logger.LoggingObject(name=__name__, logfile="data/comms.log")

        else:
            self.logger = logger_obj
            
        socket_type = kwargs.get('socket_type', 'TCP')
        if socket_type.upper() == "TCP":
            socket_type = socket.SOCK_STREAM
            
        elif socket_type.upper() == "UDP":
            socket_type = socket.SOCK_DGRAM
            
        else:
            socket_type = socket.SOCK_STREAM
            
        protocol_family = kwargs.get('protocol_family', "IPV4")
        if protocol_family.upper() == "IPV4":
            protocol_family = socket.AF_INET
            
        elif protocol_family.upper() == "IPV6":
            protocol_family = socket.AF_INET6
            
        else:
            protocol_family = socket.AF_INET
            
        self.sock_obj = socket.socket(protocol_family, socket_type)
        
    def close(self):
        """
        def close():
            close socket and kill all threads.
            
        """
        
        self.kill_signal = True
        while multitasking.config["TASKS"] != 1:
            time.sleep(0.001)
            continue
        
        multitasking.killall()
        
    @multitasking.task
    def activate_redirection_port(self):
        """
        def activate_redirection_port():
            Listen for connection on port <self.port>.

        """
    
        self.sock_obj.bind((self.broadcast_ip, self.port))
        while self.kill_signal is False:
            self.sock_obj.listen(self.max_backlog)
            self.remote_ip, self.remote_port = self.sock_obj.accept()
            request = self.sock_obj.recv(1024)
            # DEV0003

class PeerToPeer(object):
    """
    class PeerToPeer():
        Creates a connection between two peers.

        :param remote_ip type(str): The peer's IP Address or domain name.
        :param remote_port typ(int): The peer's open port for listening.
        :param connection_name type(str): The object name.

    Usage:

        from core import comms_manager

        new_connection = comms_manager.PeerToPeer("192.168.0.101", 30000, "ConnectionName")

        conn = new_connection

        conn.invite()
        conn.connect()

    """

    def __init__(self, remote_ip, remote_port, connection_name=__name__, logger_obj=None, **kwargs):
        """
        def __init__(self):
            The initialization method of PeerToPeer() class.

        """

        self.name = connection_name
        self.creation_time = time.asctime()
        self.remote_ip = remote_ip
        self.remote_port = int(remote_port)

        if logger_obj is None:
            self.logger = logger.LoggingObject(name=__name__, logfile="data/comms.log")

        else:
            self.logger = logger_obj
            
        socket_type = kwargs.get('socket_type', 'TCP')
        if socket_type.upper() == "TCP":
            socket_type = socket.SOCK_STREAM
            
        else:
            socket_type = socket.SOCK_DGRAM
            
        protocol_family = kwargs.get('protocol_family', "IPV4")
        if protocol_family.upper() == "IPV4":
            protocol_family = socket.AF_INET
            
        else:
            protocol_family = socket.AF_INET6
            
        self.sock_obj = socket.socket(protocol_family, socket_type)
            
    def kill_all(self):
        """
        def kill_all():
            Kill all threads.
        
        """
        
        multitasking.killall()
        
    @multitasking.task
    def activate_redirection_port(self, port):
        """
        def activate_redirection_port():
            Listen for connection on port <port>.

        """
        
        pass

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