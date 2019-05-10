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

        :param sock_obj type(obj): The socket to object. If sock_obj is passed,
                                   then socket_type and protocol_family is ignored.
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
        if logger_obj is None:
            self.logger = logger.LoggingObject(name=__name__, logfile="data/comms.log")

        else:
            self.logger = logger_obj

        self.logger.info("comms_manager.Main() called by {0}().".format(sys._getframe().f_back.f_code.co_name))

        self.broadcast_ip = "0.0.0.0"
        self.port = 30000
        
        # Contains: <ip>: <port> <last connection>
        # last connection is for limiting ip connection.
        self.connections = {}
        self.max_backlog = 10
        
        self.kill_signal = False
            
        self.sock_obj = kwargs.get("sock_obj", None)

        if self.sock_obj is None:
            self.logger.info("Determining socket type...")
            socket_type = kwargs.get('socket_type', 'TCP')
            if socket_type.upper() == "TCP":
                self.logger.info("Socket type is TCP.")
                socket_type = socket.SOCK_STREAM
                
            elif socket_type.upper() == "UDP":
                self.logger.info("Socket type is UDP.")
                socket_type = socket.SOCK_DGRAM
                
            else:
                self.logger.info("Unknown socket type `{0}`, using TCP instead.".format(socket_type))
                socket_type = socket.SOCK_STREAM
                
            self.logger.info("Determining protocol family...")
            protocol_family = kwargs.get('protocol_family', "IPV4")
            if protocol_family.upper() == "IPV4":
                self.logger.info("Protocol family is IPV4.")
                protocol_family = socket.AF_INET
                
            elif protocol_family.upper() == "IPV6":
                self.logger.info("Protocol family is IPV6.")
                protocol_family = socket.AF_INET6
                
            else:
                self.logger.info("Unknown protocol family, using IPV4 instead.")
                protocol_family = socket.AF_INET
                
            self.sock_obj = socket.socket(protocol_family, socket_type)
            self.logger.info("Socket `{0}` created.".format(self.name))

        else:
            self.logger.info("Using user-defined socket.")
            pass
        
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


class PeerToPeer(object):
    """
    class PeerToPeer():
        The class of comms_manager.py module that handles peer-to-peer communication.
        
        :param connection_name type(str): The object name.
        
        :param remote_ip: The IP of the remote machine.
        :param remote_port: The listening port of the remote machine.

        :param logger_obj type(object): The logger instance.

        :param sock_obj type(obj): The socket to object. If sock_obj is passed,
                                   then socket_type and protocol_family is ignored.
        :param socket_type type(str): The socket type (`TCP` or `UDP`)
        :param protocol_family type(str): The address/protocol family (`IPV4` or `IPV6`)

    Usage:

        from core import comms_manager

        new_connection = comms_manager.Main("ConnectionName")

        conn = new_connection

        conn.activate_redirection_port(30000)
        
        conn.close()

    """

    def __init__(self, connection_name=__name__, remote_ip, remote_port, logger_obj=None, **kwargs):
        """
        def __init__(self):
            The initialization method of Main() class.

        """

        self.name = connection_name
        self.creation_time = time.asctime()
        if logger_obj is None:
            self.logger = logger.LoggingObject(name=__name__, logfile="data/comms.log")

        else:
            self.logger = logger_obj

        self.logger.info("comms_manager.PeerToPeer() called by {0}().".format(sys._getframe().f_back.f_code.co_name))

        self.remote_ip = remote_ip
        self.remote_port = remote_port
        
        self.kill_signal = False
            
        self.sock_obj = kwargs.get("sock_obj", None)

        if self.sock_obj is None:
            self.logger.info("Determining socket type...")
            socket_type = kwargs.get('socket_type', 'TCP')
            if socket_type.upper() == "TCP":
                self.logger.info("Socket type is TCP.")
                socket_type = socket.SOCK_STREAM
                
            elif socket_type.upper() == "UDP":
                self.logger.info("Socket type is UDP.")
                socket_type = socket.SOCK_DGRAM
                
            else:
                self.logger.info("Unknown socket type `{0}`, using TCP instead.".format(socket_type))
                socket_type = socket.SOCK_STREAM
                
            self.logger.info("Determining protocol family...")
            protocol_family = kwargs.get('protocol_family', "IPV4")
            if protocol_family.upper() == "IPV4":
                self.logger.info("Protocol family is IPV4.")
                protocol_family = socket.AF_INET
                
            elif protocol_family.upper() == "IPV6":
                self.logger.info("Protocol family is IPV6.")
                protocol_family = socket.AF_INET6
                
            else:
                self.logger.info("Unknown protocol family, using IPV4 instead.")
                protocol_family = socket.AF_INET
                
            self.sock_obj = socket.socket(protocol_family, socket_type)
            self.logger.info("Socket `{0}` created.".format(self.name))

        else:
            self.logger.info("Using user-defined socket.")
            pass
        
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

    def invite(self):
        """
        def invite():
            Send <remote_ip> a "friend request".

        """

        # DEV0003