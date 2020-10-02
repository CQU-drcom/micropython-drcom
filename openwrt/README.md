# openwrt-micropython-drcom

链接该文件夹到 [OpenWrt SDK](https://openwrt.org/docs/guide-developer/using_the_sdk) 的 `package/network/micropython-drcom`，在 OpenWrt SDK 目录运行

```bash
make package/micropython-drcom/compile
```

之后便可在 `bin/packages/*/base/` 下得到 micropython-drcom 的两个包：

- `micropython-drcom`: 依赖于 `micropython-lib` 包，连同依赖安装后会比 `micropython-drcom-with-lib` 大；
- `micropython-drcom-with-lib`: 内有裁剪过的 micropython-lib，所以不依赖于 `micropython-lib` 包，如果没有其余使用 `micropython-lib` 包的需求，推荐使用该包以减少体积。
