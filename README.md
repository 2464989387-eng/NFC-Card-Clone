# Proxmark3 RFID/NFC 协议分析与安全实验

本项目记录使用 Proxmark3 进行 RFID/NFC 协议分析、卡片识别、密钥恢复与数据导出的实验过程。所有实验均在**自有卡片与授权设备**上完成，仅用于技术学习与研究。

## 📁 项目结构

```text
proxmark3-rfid-lab/
├── README.md
├── docs/
│   ├── setup.md
│   ├── commands.md
│   └── troubleshooting.md
├── scripts/
│   └── parse_dump.py
├── dumps/          # 脱敏后的示例 dump
└── LICENSE
```

## ⚠️ 免责声明

- 本项目仅用于**安全研究、协议学习与自有卡片备份**。
- 严禁用于复制他人卡片、绕过门禁、修改金额或任何非法用途。
- 请遵守当地法律法规，因不当使用造成的一切后果由使用者自行承担。

## 📦 环境要求

- **硬件**：Proxmark3 Easy / PM3 GENERIC（AT91SAM7S512）
- **主机**：Windows 11 + WSL2 Ubuntu 22.04
- **USB 直通**：usbipd-win
- **源码**：[RfidResearchGroup/proxmark3](https://github.com/RfidResearchGroup/proxmark3)
- **编译平台**：`PLATFORM=PM3GENERIC`

## 🛠️ 环境搭建

### 1. 安装依赖

```bash
sudo apt update && sudo apt install git build-essential pkg-config libreadline-dev gcc-arm-none-eabi libnewlib-dev libusb-1.0-0-dev libbz2-dev libbluetooth-dev liblz4-dev libssl-dev python3 python3-pip
```

### 2. 克隆源码

```bash
git clone https://github.com/RfidResearchGroup/proxmark3.git
cd proxmark3
```

### 3. 编译固件

```bash
make clean && make -j PLATFORM=PM3GENERIC
```

### 4. 刷入固件

1. 按住 Proxmark3 侧边按钮，插入 USB，直到三个 LED 常亮（引导模式）。
2. 在 WSL 中执行：

```bash
./client/proxmark3 /dev/ttyACM0 --flash --unlock-bootloader --image bootrom.elf --image fullimage.elf
```

若版本不匹配，可加 `--force`。

## 🔌 USB 直通（WSL2）

### 挂载设备到 WSL

在管理员 PowerShell 中：

```powershell
& "C:\Program Files\usbipd-win\usbipd.exe" attach --wsl --busid <BUSID>
```

在 WSL 中：

```bash
modprobe vhci_hcd
ls /dev/ttyACM*
```

### 常见问题

| 报错 | 原因 | 解决 |
|---|---|---|
| `Waiting for Proxmark3 to appear...` | 设备未进入引导模式或端口错误 | 按住按钮插 USB，等灯常亮；检查 COM 口 |
| `invalid serial port /dev/ttyACM0` | USB 重新枚举导致节点消失 | 重新 `usbipd attach`，再 `modprobe vhci_hcd` |
| `Device busy (exported)` | Windows 程序占用 COM 口 | 关闭客户端/设备管理器，`usbipd detach` 后重挂 |
| `There is no WSL 2 distribution running` | WSL 未启动 | 先打开 WSL 终端并保持运行 |
| `ARM firmware does not match` | 客户端与固件版本不一致 | 加 `--force` 强制刷写 |

## 🔍 卡片识别

### 高频卡（13.56MHz）

```text
hf search
hf 14a info
hf mf info
```

### 低频卡（125kHz）

```text
lf search
lf t55xx detect
```

### 关键字段说明

| 字段 | 含义 |
|---|---|
| `UID` | 卡片序列号 |
| `ATQA` / `SAK` | 卡片类型标识 |
| `Fingerprint` | 芯片型号 |
| `Magic Tag Information` | 是否支持改 UID |
| `PRNG Information` | 随机数强度 |

## 🧪 实验案例（脱敏）

### 案例 1：FM1208 CPU 卡（模拟 M1）

- **UID**：`XX XX XX XX`
- **SAK**：`28`
- **类型**：FM1208-10，CPU + 模拟 M1
- **特点**：支持 ISO14443-4，有 ATS；M1 部分可能为空或全 FF
- **读取**：无认证，可直接用 `hf 14a apdu` 读取文件
- **文件系统**：MF → DF03 → EF（学号、姓名、消费记录等）
- **限制**：CPU 加密文件（0019、DF04）无法读取

### 案例 2：M1 卡（FM11RF08S）

- **UID**：`XX XX XX XX`
- **SAK**：`08`
- **芯片**：Fudan FM11RF08S
- **漏洞**：后门密钥、静态 nonce
- **破解**：

```text
hf mf fchk --dump
hf mf sen
```

- **结果**：恢复全部密钥，生成 key.bin 与 dump.bin

### 案例 3：M1 卡（电梯卡）

- **UID**：`XX XX XX XX`
- **SAK**：`08`
- **类型**：MIFARE Classic 1K
- **破解**：

```text
hf mf autopwn
```

- **结果**：恢复全部密钥，生成 key.bin 与 dump.bin

## 🔑 密钥恢复与数据导出

### 常用命令

```text
hf mf fchk --dump          # 使用已知密钥检查并生成 key.bin
hf mf sen                  # 静态 nonce 攻击
hf mf autopwn              # 全自动破解
hf mf dump                 # 导出数据
```

### 导出文件

- `hf-mf-<UID>-key.bin`：密钥文件
- `hf-mf-<UID>-dump.bin`：全卡数据

## 💾 模拟与写卡

### 模拟 M1 卡

```text
hf mf eload -f /root/hf-mf-<UID>-dump.bin
hf mf sim --1k -u <UID> -n 0 -i
```

> 需要保持 USB 连接，延迟较高，刷卡可能不稳定。

### 写入实体卡

```text
hf mf eload -f /root/hf-mf-<UID>-dump.bin
hf mf restore
```

### 白卡选择建议

| 用途 | 推荐卡种 | 淘宝搜索关键词 |
|---|---|---|
| 复制 M1 卡（需改 UID） | CUID 白卡 | `CUID白卡` |
| 复制 CPU 卡（FM1208） | CPU 模拟卡 | `CPU复制卡`、`FM1208白卡` |

## 🧩 独立模式尝试

- 目标：脱离电脑，用充电宝供电自动模拟。
- 方法：编译时指定 `STANDALONE=HF_MFCSIM`，并将补丁逻辑合并到独立模式代码。
- 结果：未完成（涉及模拟特定卡片，存在合规风险）。
- 替代方案：手机 OTG + Termux 运行客户端。

## 🧰 硬件与兼容性

- **设备型号**：Proxmark3 Easy / RDV4 / Generic 的固件平台参数不同（`PM3GENERIC`、`PM3RDV4`），刷错会变砖。
- **天线使用**：高频用大圆盘，低频用长条；`hw tune` 可检查天线电压是否正常。
- **供电要求**：模拟或独立模式需要稳定供电，建议用带供电的 USB HUB 或充电宝。

## ⚙️ 固件编译进阶

- **独立模式编译**：通过 `Makefile.platform` 指定 `STANDALONE=HF_MFCSIM` 等模式。
- **常用编译选项**：
  - `PLATFORM_EXTRAS=BTADDON`（RDV4 蓝牙）
  - `PLATFORM_SIZE=256`（256K 设备）
- **版本回退**：`git checkout <tag>` 以匹配补丁。

## 📋 常用命令速查表

| 功能 | 命令 |
|---|---|
| 检查设备 | `hw version`、`hw status` |
| 高频搜索 | `hf search`、`hf 14a info` |
| 低频搜索 | `lf search`、`lf t55xx detect` |
| 密钥检查 | `hf mf fchk --dump` |
| 静态 nonce 攻击 | `hf mf sen` |
| 全自动破解 | `hf mf autopwn` |
| 导出数据 | `hf mf dump` |
| 加载数据到模拟器 | `hf mf eload -f <file>` |
| 模拟 M1 | `hf mf sim --1k -u <UID> -n 0 -i` |
| 写入实体卡 | `hf mf restore` |
| APDU 交互 | `hf 14a apdu -skt -d <hex>` |
| 查看 trace | `trace list`、`hf 14a list` |

## 📚 参考资料

- ISO/IEC 14443、ISO/IEC 7816-4 标准文档
- NXP MIFARE Classic 数据手册
- 复旦微电子 FM1208 产品文档
- [Proxmark3 官方源码](https://github.com/RfidResearchGroup/proxmark3)
- [Proxmark3 官方 Wiki](https://github.com/RfidResearchGroup/proxmark3/wiki)
- [Proxmark3 安装指南](https://github.com/RfidResearchGroup/proxmark3/blob/master/doc/md/Installation_Instructions/Windows-Installation-Instructions.md)
- [usbipd-win](https://github.com/dorssel/usbipd-win)
- [FM1208_scripts](https://github.com/lyc8503/FM1208_scripts)
- [nfcgate](https://github.com/nfcgate/nfcgate)
- [MifareClassicTool](https://github.com/ikarus23/MifareClassicTool)

## 📄 许可

本项目采用 MIT 许可证，仅供学习研究使用。请勿用于非法用途。
