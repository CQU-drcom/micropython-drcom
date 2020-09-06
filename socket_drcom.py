from time import sleep
import threading
from socket import *
import os
_socket = socket
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
exec("""
class socket(_socket):
    def __init__(self,*a,**b):
        super().__init__(*a, **b)
        self.killtimeout=0
    def setkilltimeout(self, timeout):
        self.killtimeout=timeout
""" + "".join(("""
    def {method}(self, *a, **b):
        if self.killtimeout:
            killer = timeoutKiller(self.killtimeout)
        super().{method}(*a,**b)
        if self.killtimeout:
            killer.release()
""".format(method=method) for method in _timeout_methods)))
"""
自动地生成类：
class socket(socket_):
    def __init__(self,*a,**b):
        super().__init__(*a, **b)

    def setkilltimneout(self, timeout):
        self.killtimeout=timeout

    def {method}(self, *a, **b):
        if self.killtimeout:
            killer = timeoutKiller(self.killtimeout)
        super().{method}(*a,**b)
        if self.killtimeout:
            killer.release()

"""
