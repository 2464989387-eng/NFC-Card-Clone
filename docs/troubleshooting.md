# 常见问题与排查

| 报错 | 原因 | 解决 |
|---|---|---|
| `Waiting for Proxmark3 to appear...` | 设备未进入引导模式或端口错误 | 按住按钮插 USB，等灯常亮；检查 COM 口 |
| `invalid serial port /dev/ttyACM0` | USB 重新枚举导致节点消失 | 重新 `usbipd attach`，再 `modprobe vhci_hcd` |
| `Device busy (exported)` | Windows 程序占用 COM 口 | 关闭客户端/设备管理器，`usbipd detach` 后重挂 |
| `There is no WSL 2 distribution running` | WSL 未启动 | 先打开 WSL 终端并保持运行 |
| `ARM firmware does not match` | 客户端与固件版本不一致 | 加 `--force` 强制刷写 |
| 天线无响应 | 连接松动或位置不对 | 检查天线，`hw tune`，换卡位置 |
| 写卡失败 | 白卡类型不对或 UID 不可改 | 确认白卡为 CUID/FUID，容量足够 |
