# -*- coding: utf-8 -*-
"""
Connect to a remote host and tunnel a port.
"""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2023-2026 Sven Sager"
__license__ = "GPLv2"

import asyncio
import threading
from logging import getLogger
from typing import Tuple, Union

import asyncssh

log = getLogger("ssh_tunneling")


class SSHLocalTunnel:

    def __init__(self, remote_target: Union[int, str], ssh_host: str, ssh_port: int = 22):
        """
        Connect to a ssh remote host and tunnel a port or unix socket to your host.

        :param remote_target: Port or unix socket path on the remote host to tunnel through ssh
        :param ssh_host: ssh remote host address
        :param ssh_port: ssh remote host port
        """
        self._remote_target = remote_target
        self._ssh_host = ssh_host
        self._ssh_port = ssh_port

        self._loop: asyncio.AbstractEventLoop | None = None
        self._stop_event: asyncio.Event | None = None
        self._thread: threading.Thread | None = None

        self._started = threading.Event()
        self._stopped = threading.Event()

        self._startup_error: Exception | None = None
        self._runtime_error: Exception | None = None

        self._conn: asyncssh.SSHClientConnection | None = None
        self._server: asyncssh.SSHForwarder | None = None
        self._local_tunnel_port: int | None = None

    def _thread_main(self, username, password=None, client_keys=None, passphrase=None):
        try:
            asyncio.run(self._run(username, password, client_keys, passphrase))
        except Exception as exc:
            if not self._started.is_set():
                self._startup_error = exc
                self._started.set()
            else:
                self._runtime_error = exc
        finally:
            self._stopped.set()

    async def _run(self, username, password=None, client_keys=None, passphrase=None):
        self._loop = asyncio.get_running_loop()
        self._stop_event = asyncio.Event()

        try:
            async with asyncssh.connect(
                host=self._ssh_host,
                port=self._ssh_port,
                username=username,
                password=password,
                client_keys=client_keys,
                passphrase=passphrase,
                known_hosts=None,  # Analog zu MissingHostKeyPolicy()
                config=None,  # Do not parse local config
            ) as conn:
                self._conn = conn
                # Forward local port 0 (dynamic) to remote target (port or unix socket)
                if isinstance(self._remote_target, int):
                    self._server = await conn.forward_local_port(
                        '127.0.0.1', 0, '127.0.0.1', self._remote_target
                    )
                else:
                    self._server = await conn.forward_local_port_to_path(
                        '127.0.0.1', 0, self._remote_target
                    )
                self._local_tunnel_port = self._server.get_port()

                self._started.set()
                await self._stop_event.wait()

                self._server.close()
                await self._server.wait_closed()

        except Exception as exc:
            if not self._started.is_set():
                self._startup_error = exc
                self._started.set()
                return
            raise

    def connect_by_credentials(self, username: str, password: str) -> int:
        """
        Connect to a ssh remote host and tunnel specified port of localhost.

        :return: Local port on wich the remote port is connected
        """
        if self._thread and self._thread.is_alive():
            raise RuntimeError("Already connected")

        self._started.clear()
        self._stopped.clear()
        self._startup_error = None
        self._runtime_error = None

        self._thread = threading.Thread(
            target=self._thread_main,
            args=(username, password),
            daemon=True
        )
        self._thread.start()

        if not self._started.wait(20.0):
            self.disconnect()
            raise TimeoutError("SSH connection timed out")

        if self._startup_error:
            error = self._startup_error
            self.disconnect()
            raise error

        return self._local_tunnel_port

    def connect_by_keyfile(self, username: str, key_file: str, key_password: str = None) -> int:
        """
        Connect to a ssh remote host and tunnel specified port of localhost.

        :return: Local port on wich the remote port is connected
        """
        if self._thread and self._thread.is_alive():
            raise RuntimeError("Already connected")

        self._started.clear()
        self._stopped.clear()
        self._startup_error = None
        self._runtime_error = None

        self._thread = threading.Thread(
            target=self._thread_main,
            args=(username, None, [key_file], key_password),
            daemon=True
        )
        self._thread.start()

        if not self._started.wait(20.0):
            self.disconnect()
            raise TimeoutError("SSH connection timed out")

        if self._startup_error:
            error = self._startup_error
            self.disconnect()
            raise error

        return self._local_tunnel_port

    def disconnect(self):
        """Close SSH tunnel connection."""
        if self._loop and self._stop_event:
            self._loop.call_soon_threadsafe(self._stop_event.set)

        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5.0)

        self._conn = None
        self._server = None
        self._local_tunnel_port = None
        self._thread = None
        self._loop = None
        self._stop_event = None

    @staticmethod
    def key_file_password_protected(key_file: str) -> bool:
        # asyncssh doesn't have a direct equivalent without trying to load it.
        # But we can try to load it with an empty passphrase.
        try:
            asyncssh.read_private_key(key_file, passphrase=None)
            return False
        except asyncssh.KeyImportError:
            return True
        except Exception:
            return True

    def send_cmd(self, cmd: str, timeout: float = None, stdin: str = None) -> Union[Tuple[str, str, int], Tuple[None, None, None]]:
        """
        Send simple command to ssh host.

        :param cmd: Shell command to execute on remote host
        :param timeout: Timeout for execution
        :param stdin: Send this string to stdin
        :return: Tuple with stdout, stderr, exit status
        """
        if not self.connected:
            raise RuntimeError("Not connected")

        # Running async command from sync context
        async def _exec():
            result = await self._conn.run(cmd, timeout=timeout, input=stdin)
            return result.stdout, result.stderr, result.exit_status

        try:
            future = asyncio.run_coroutine_threadsafe(_exec(), self._loop)
            stdout, stderr, exit_status = future.result(timeout=timeout)
            if type(stdout) is bytes:
                stdout = stdout.decode(errors="ignore")
            if type(stderr) is bytes:
                stderr = stderr.decode(errors="ignore")
            return stdout, stderr, exit_status
        except Exception as e:
            log.error(e)
            return None, None, None

    @property
    def connected(self):
        """Check connection state of ssh tunnel."""
        return self._conn is not None and self._started.is_set() and not self._stopped.is_set()

    @property
    def local_tunnel_port(self) -> int:
        return self._local_tunnel_port
