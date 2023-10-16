from typing import Any

import zmq
from draugr.python_utilities import in_docker
from warg import AlsoDecorator

__all__ = ["QliveClient"]


def default_address() -> str:
    if in_docker():
        return "tcp://host.docker.internal:5555"
    return "tcp://localhost:5555"


class QliveClient(AlsoDecorator):
    """
    TODO: MAYBE NOT ALSO A DECORATOR

    Client for sending data to qgis instance
    """

    def __init__(self, address: str = default_address()):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)

        if not address:
            address = default_address()

        if str.isnumeric(address):  # only port was given
            address = f"{default_address().split(':')[0]}{address}"

        if "://" not in address:  # protocol is missing
            address = f"tcp://{address}"

        self.address = address

        self.blocking = False
        self.flag = None
        if not self.blocking:
            self.poller = zmq.Poller()
            self.flag = zmq.NOBLOCK
            self.wait_time = 1000
            self.poller.register(self.socket, zmq.POLLIN)

    def __enter__(self):
        self.socket.connect(self.address)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.close()

    def send(self, *args) -> Any:
        self.socket.send(*args, self.flag)

        if self.blocking:
            return self.socket.recv()

        socks = dict(self.poller.poll(self.wait_time))
        if socks:
            if socks.get(self.socket) == zmq.POLLIN:
                return self.socket.recv(self.flag)

        return  # TODO: just ignore for now
        raise TimeoutError
