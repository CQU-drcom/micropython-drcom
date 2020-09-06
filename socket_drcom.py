from time import sleep
import threading
from socket import *
import usocket as _socket
import os
__socket = socket
del socket


class timeoutKiller(threading.Thread):
    def __init__(self, timeout):
        super().__init__()
        self.timeout = timeout
        self.ok = 0
        self.start()

    def run(self):
        count = int(self.timeout)
        for i in range(count):
            sleep(1)
            if self.ok:
                return
        sleep(self.timeout - count)
        if not self.ok:
            print("Socket timeout!")
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


exec("""
class socket(socketRecvfromFixed):
    def __init__(self,*a,**b):
        super().__init__(*a, **b)
        self.killtimeout=0
    def setkilltimeout(self, timeout):
        self.killtimeout=timeout
""" + "".join(("""
    def {method}(self, *a, **b):
        if self.killtimeout:
            killer = timeoutKiller(self.killtimeout)
        rst = super().{method}(*a,**b)
        if self.killtimeout:
            killer.release()
        return rst
""".format(method=method) for method in _timeout_methods)))
"""
自动地生成类：
class socket(socketRecvfromFixed):
    def __init__(self,*a,**b):
        super().__init__(*a, **b)

    def setkilltimneout(self, timeout):
        self.killtimeout=timeout

    def {method}(self, *a, **b):
        if self.killtimeout:
            killer = timeoutKiller(self.killtimeout)
        rst = super().{method}(*a,**b)
        if self.killtimeout:
            killer.release()
        return rst

"""
