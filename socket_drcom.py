from time import sleep
import threading
from socket import *
import usocket as _socket
import os
__socket = socket
del socket
max_threads = 32
thread_delay = 1 / max_threads
log = lambda x: print(x)


class timeoutKiller(threading.Thread):
    def __init__(self, timeout):
        super().__init__()
        self.timeout = timeout
        self.ok = 0
        sleep(thread_delay)
        self.start()

    def run(self):
        count = int(self.timeout)
        for i in range(count):
            sleep(1)
            if self.ok:
                return
        sleep(self.timeout - count)
        if not self.ok:
            log('[socket]', "Socket timeout! Kill drcom.")
            os.kill(os.getpid(), 15)

    def release(self):
        self.ok = 1


_timeout_methods = ('accept', 'bind', 'connect', 'sendall', 'sendto',
                    'recvfrom')


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
        self.killtimeout = timeout

    def getkilltimeout(self):
        return self.killtimeout

    def _run_with_timeout(self, func, a, b):
        if self.killtimeout:
            killer = timeoutKiller(self.killtimeout)
        try:
            rst = func(*a, **b)
        finally:
            if self.killtimeout:
                killer.release()
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
