# 环境搭建

## 硬件要求

- Proxmark3 Easy / PM3 GENERIC（AT91SAM7S512）
- USB 数据线（支持数据传输）
- 高频天线（大圆盘）、低频天线（长条）

## 软件环境

- Windows 11 + WSL2 Ubuntu 22.04
- usbipd-win
- 源码：[RfidResearchGroup/proxmark3](https://github.com/RfidResearchGroup/proxmark3)

## 安装依赖

```bash
sudo apt update && sudo apt install git build-essential pkg-config libreadline-dev gcc-arm-none-eabi libnewlib-dev libusb-1.0-0-dev libbz2-dev libbluetooth-dev liblz4-dev libssl-dev python3 python3-pip
```

## 克隆源码

```bash
git clone https://github.com/RfidResearchGroup/proxmark3.git
cd proxmark3
```

## 编译固件

```bash
make clean && make -j PLATFORM=PM3GENERIC
```

## 刷入固件

1. 按住 Proxmark3 侧边按钮，插入 USB，直到三个 LED 常亮（引导模式）。
2. 在 WSL 中执行：

```bash
./client/proxmark3 /dev/ttyACM0 --flash --unlock-bootloader --image bootrom.elf --image fullimage.elf
```

若版本不匹配，可加 `--force`。

## USB 直通（WSL2）

在管理员 PowerShell 中：

```powershell
& "C:\Program Files\usbipd-win\usbipd.exe" attach --wsl --busid <BUSID>
```

在 WSL 中：

```bash
modprobe vhci_hcd
ls /dev/ttyACM*
```
