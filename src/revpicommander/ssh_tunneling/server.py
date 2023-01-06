# -*- coding: utf-8 -*-
"""
Connect to a remote host and tunnel a port.

This was crated on base of the paramiko library demo file forward.py, see on
GitHub https://github.com/paramiko/paramiko/blob/main/demos/forward.py
"""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2023 Sven Sager"
__license__ = "GPLv3"

import select
from socketserver import BaseRequestHandler, ThreadingTCPServer
from threading import Thread

from paramiko.client import SSHClient, WarningPolicy
from paramiko.rsakey import RSAKey
from paramiko.ssh_exception import PasswordRequiredException
from paramiko.transport import Transport


class ForwardServer(ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True


class Handler(BaseRequestHandler):
    def handle(self):
        try:
            chan = self.ssh_transport.open_channel(
                "direct-tcpip",
                (self.chain_host, self.chain_port),
                self.request.getpeername(),
            )
        except Exception as e:
            return
        if chan is None:
            return

        while True:
            r, w, x = select.select([self.request, chan], [], [], 5.0)
            if self.request in r:
                data = self.request.recv(1024)
                if len(data) == 0:
                    break
                chan.send(data)
            if chan in r:
                data = chan.recv(1024)
                if len(data) == 0:
                    break
                self.request.send(data)

        chan.close()
        self.request.close()


class SSHLocalTunnel:

    def __init__(self, remote_tunnel_port: int, ssh_host: str, ssh_port: int = 22):
        """
        Connect to a ssh remote host and tunnel a port to your host.

        :param remote_tunnel_port: Port on the remote host to tunnel through ssh
        :param ssh_host: ssh remote host address
        :param ssh_port: ssh remote host port
        """
        self._remote_tunnel_port = remote_tunnel_port
        self._ssh_host = ssh_host
        self._ssh_port = ssh_port

        self._th_server = Thread()

        self._ssh_client = SSHClient()
        self._ssh_client.load_system_host_keys()
        self._ssh_client.set_missing_host_key_policy(WarningPolicy())

        self._ssh_transport = None  # type: Transport
        self._forward_server = None  # type: ThreadingTCPServer
        self._local_tunnel_port = None  # type: int

    def __th_target(self):
        """Server thread for socket mirror."""
        self._forward_server.serve_forever()

    def _configure_forward_server(self) -> int:
        """
        Configure forward server for port mirror.

        :return: Local port on wich the remote port is connected
        """
        self._ssh_transport = self._ssh_client.get_transport()

        class SubHandler(Handler):
            chain_host = "127.0.0.1"
            chain_port = self._remote_tunnel_port
            ssh_transport = self._ssh_transport

        self._forward_server = ForwardServer(("127.0.0.1", 0), SubHandler)
        self._local_tunnel_port = self._forward_server.socket.getsockname()[1]

        self._th_server = Thread(target=self.__th_target)
        self._th_server.start()

        return self._local_tunnel_port

    def connect_by_credentials(self, username: str, password: str) -> int:
        """
        Connect to a ssh remote host and tunnel specified port of localhost.

        :return: Local port on wich the remote port is connected
        """
        if self._th_server.is_alive():
            raise RuntimeError("Already connected")

        self._ssh_client.connect(
            hostname=self._ssh_host,
            port=self._ssh_port,
            username=username,
            password=password,
        )

        return self._configure_forward_server()

    def connect_by_keyfile(self, username: str, key_file: str, key_password: str = None) -> int:
        """
        Connect to a ssh remote host and tunnel specified port of localhost.

        :return: Local port on wich the remote port is connected
        """
        if self._th_server.is_alive():
            raise RuntimeError("Already connected")

        if self.key_file_password_protected(key_file):
            private_key = RSAKey.from_private_key_file(key_file, key_password)
        else:
            private_key = RSAKey.from_private_key_file(key_file)

        self._ssh_client.connect(
            hostname=self._ssh_host,
            port=self._ssh_port,
            username=username,
            pkey=private_key,
            look_for_keys=True,
        )

        return self._configure_forward_server()

    def disconnect(self):
        """Close SSH tunnel connection."""
        self._local_tunnel_port = None
        if self._forward_server:
            self._forward_server.shutdown()
            self._forward_server.server_close()
        if self._ssh_transport:
            self._ssh_transport.close()
        self._ssh_client.close()

    @staticmethod
    def key_file_password_protected(key_file: str) -> bool:
        try:
            RSAKey.from_private_key_file(key_file)
        except PasswordRequiredException:
            return True
        return False

    @property
    def connected(self):
        """Check connection state of ssh tunnel."""
        return self._ssh_transport and self._ssh_transport.is_active()

    @property
    def local_tunnel_port(self) -> int:
        return self._local_tunnel_port
