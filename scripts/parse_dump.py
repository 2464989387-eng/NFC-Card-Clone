#!/usr/bin/env python3
"""
解析 MIFARE Classic dump 文件，提取 UID、SAK、ATQA 和扇区数据。
用法: python3 parse_dump.py <dump.bin>
"""

import sys
import struct


def parse_dump(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    if len(data) < 1024:
        print("文件大小不足 1024 字节，可能不是完整的 1K 卡 dump。")
        return
    # Block 0: UID (4 bytes), SAK, ATQA
    uid = data[0:4].hex().upper()
    sak = data[5]
    atqa = struct.unpack('<H', data[6:8])[0]
    print(f"UID: {uid}")
    print(f"SAK: {sak:02X}")
    print(f"ATQA: {atqa:04X}")
    print("\n扇区数据:")
    for sector in range(16):
        print(f"--- 扇区 {sector} ---")
        for block in range(4):
            offset = (sector * 4 + block) * 16
            block_data = data[offset:offset+16]
            print(f"块 {sector*4+block:02d}: {block_data.hex().upper()}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python3 parse_dump.py <dump.bin>")
        sys.exit(1)
    parse_dump(sys.argv[1])
