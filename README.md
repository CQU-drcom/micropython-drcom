# micropython-drcom

DrCOM 非官方客户端，修改自 [drcom-generic](https://github.com/drcoms/drcom-generic) 以使其能够在 OpenWrt 软件源中的 [micropython](https://github.com/micropython/micropython) 软件包中运行。

（注：[micropython](https://github.com/micropython/micropython) 是一种 python 3.x 的实现，体积较小，相较 cpython 更适合在运行在一些存储空间非常有限的路由器上，但未实现 python 标准库中的全部功能。）

**Testing needed**

以下文件用于补齐 drcom-generic 需要但 micropython 未实现的 python 标准库中的部分内容

- [md5\_drcom.py](md5_drcom.py): `hashlib.md5`的纯 python 实现，来自 pypy
- [random\_drcom.py](random_drcom.py): `random.randint`的实现
- [socket\_drcom.py](socket_drcom,py): 提供了处理 socket 连接超时的 workaround

## 连接超时时的行为

OpenWrt 官方软件源的部分或全部架构下的 micropython 的 socket 类中无`settimeout`方法。此处 [socket\_drcom.py](socket_drcom.py) 提供了一种 workaround：在超时时杀掉自己。

## 感谢

感谢 [drcom-generic](https://github.com/micropython/micropython) 项目和 [https://github.com/micropython/micropython](micropython) 项目。
