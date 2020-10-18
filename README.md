# micropython-drcom

DrCOM 非官方客户端，修改自 [drcom-generic](https://github.com/drcoms/drcom-generic) 以使其能够在 OpenWrt 软件源中的 [micropython](https://github.com/micropython/micropython) 软件包中运行。

另有 opkg 进行打包于 [openwrt](openwrt)。

**WIP & Testing needed**

## 关于 micropython

[micropython](https://github.com/micropython/micropython) 是一种 python 3.x 的实现，体积较小，相较 cpython 更适合在运行在一些存储空间非常有限的路由器上，但未实现 python 标准库中的全部功能。

在 OpenWrt 官方源中有两个包：

- [micropython](https://openwrt.org/packages/pkgdata/micropython): micropython 解释器，x86 架构的`1.9.4-2`版安装后仅 365.1K
- [micropython-lib](https://openwrt.org/packages/pkgdata/micropython-lib): 提供不完整实现的 python 标准库，`1.9.4-2`版安装后达 1.1M。[micropython](micropython) 文件夹中是被 drcom-generic 脚本依赖的部分，共 168K，将内容复制至 `/usr/lib/micropython` 或与 [latest-wired-micropython.py](latest-wired-micropython.py) 置于同一目录来使用，以省下完整 micropython-lib 的其余部分所需的空间。

以下文件用于补齐 drcom-generic 需要但 micropython 未实现的 python 标准库中的部分内容

- [md5\_drcom.py](md5_drcom.py): `hashlib.md5`的纯 python 实现，来自 pypy，为了与 python 3.x 兼容作了细微更改
- [random\_drcom.py](random_drcom.py): `random.randint`的实现
- [socket\_drcom.py](socket_drcom,py): 提供了处理 socket 连接超时的 workaround

## 与原版 drcom-generic 脚本的差别

### socket 传输超时处理

OpenWrt 官方软件源的部分或全部架构（未作考究）下的 micropython 的 socket 类中无`settimeout`方法。此处 [socket\_drcom.py](socket_drcom.py) 提供了一种 workaround：在超时时杀掉自己，并输出`Socket timeout! Kill drcom.`（如果设置了保存日志，也会写到日志里）。

不再试图捕获超时的异常。

清空 socket buffer 的方法从捕获超时异常改为使用非阻塞 socket。

### 配置文件

（一定程度是为了便于打包成 ipk）[latest-wired-micropython.py](latest-wired-micropython.py) 启动时默认会读取 `/etc/drcom_wired.conf` 作为配置文件，亦可通过传入文件路径作为参数来指定其他位置的配置文件，从而更改登陆信息不需要更改脚本源码。兼容 drcom-generic 的 python2、python3 版以及 [dogcom](https://github.com/mchome/dogcom) 的配置。

除了登陆信息，另有有以下配置项：

- `PID_ENABLE`: `bool`，默认`True`，是否启用 pid 文件
- `PID_PATH`: `str`，默认`'/var/run/drcom.pid'`，pid 文件路径
- `DEBUG`: `bool`，默认`False`，是否开启日志文件
- `LOG_PATH`: `str`，默认`'/tmp/drcom_client.log'`，日志文件路径

### 错误信息

micropython 的报错没有 cpython 那么详细

## 感谢

感谢 [drcom-generic](https://github.com/micropython/micropython) 项目和 [micropython](https://github.com/micropython/micropython) 项目。
