# 常用命令速查

## 设备检查

```text
hw version
hw status
hw tune
```

## 高频卡（13.56MHz）

```text
hf search
hf 14a info
hf mf info
hf mf fchk --dump
hf mf sen
hf mf autopwn
hf mf dump
hf mf eload -f <file>
hf mf sim --1k -u <UID> -n 0 -i
hf mf restore
hf 14a apdu -skt -d <hex>
```

## 低频卡（125kHz）

```text
lf search
lf t55xx detect
```

## Trace 分析

```text
trace list
hf 14a list
```
