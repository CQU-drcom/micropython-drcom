from socket import *
import usocket as _socket
import os
import signal
import ffilib

alarm = ffilib.libc().func("I", "alarm", "I")
__socket = socket
del socket
log = lambda x: print(x)

_timeout_methods = ('accept', 'bind', 'connect', 'sendall', 'sendto',
                    'recvfrom')


class timeout(OSError):
    pass


def timeout_handler(sig):
    raise timeout()


signal.signal(14, timeout_handler)


class socketRecvfromFixed(__socket):
    def __init__(self, *a, **b):
        super().__init__(*a, **b)

    def recvfrom(self, *a, **b):
        s, addr = super().recvfrom(*a, **b)
        addr = _socket.sockaddr(addr)
        return (s, (_socket.inet_ntop(addr[0], addr[1]), addr[2]))


class socket(socketRecvfromFixed):
    def __init__(self, *a, **b):
        super().__init__(*a, **b)
        self.killtimeout = 0

    def setkilltimeout(self, timeout):
        self.killtimeout = int(timeout)

    def getkilltimeout(self):
        return self.killtimeout

    def _run_with_timeout(self, func, a, b):
        alarm(self.killtimeout)
        rst = func(*a, **b)
        alarm(0)
        return rst

    def accept(self, *a, **b):
        return self._run_with_timeout(super().accept, a, b)

    def bind(self, *a, **b):
        return self._run_with_timeout(super().bind, a, b)

    def connect(self, *a, **b):
        return self._run_with_timeout(super().connect, a, b)

    def sendall(self, *a, **b):
        return self._run_with_timeout(super().sendall, a, b)

    def sendto(self, *a, **b):
        return self._run_with_timeout(super().sendto, a, b)

    def recvfrom(self, *a, **b):
        return self._run_with_timeout(super().recvfrom, a, b)
