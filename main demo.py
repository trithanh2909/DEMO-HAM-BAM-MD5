#!/usr/bin/env python3
"""Bản triển khai MD5 phục vụ học tập theo RFC 1321.

Cảnh báo: MD5 không còn an toàn cho các ứng dụng cần khả năng chống va chạm.
Chương trình này chỉ dùng để học thuật toán, kiểm thử và minh họa tính toàn vẹn.
Phần lõi md5() tự thực hiện thuật toán; hashlib chỉ được gọi trong self_test()
để đối chiếu kết quả, không dùng để tạo digest trong chức năng chính.
"""

from __future__ import annotations

import hashlib
import hmac
import math
import struct
import sys
import tempfile
from pathlib import Path
from typing import Any

# ============================================================================
# PHẦN 1. HẰNG SỐ VÀ CÁC PHÉP TOÁN CƠ BẢN CỦA MD5
# ============================================================================

_MASK32 = 0xFFFFFFFF

# Lịch xoay trái: 4 vòng, mỗi vòng 16 bước.
_SHIFT = (
    [7, 12, 17, 22] * 4
    + [5, 9, 14, 20] * 4
    + [4, 11, 16, 23] * 4
    + [6, 10, 15, 21] * 4
)

# T[i] = floor(2^32 * abs(sin(i))), i = 1..64; góc tính theo radian.
_K = [int(abs(math.sin(i + 1)) * (1 << 32)) & _MASK32 for i in range(64)]

# Bốn từ trạng thái khởi tạo theo RFC 1321.
_INITIAL_STATE = (0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476)


def _left_rotate(value: int, amount: int) -> int:
    """Xoay trái một giá trị trong phạm vi 32 bit."""
    value &= _MASK32
    return ((value << amount) | (value >> (32 - amount))) & _MASK32


def _pad(message: bytes) -> bytes:
    """Đệm thông điệp: bit 1, các bit 0, rồi độ dài ban đầu 64 bit little-endian."""
    original_length_bits = (len(message) * 8) & 0xFFFFFFFFFFFFFFFF
    padded = bytearray(message)
    padded.append(0x80)

    while len(padded) % 64 != 56:
        padded.append(0)

    padded.extend(struct.pack("<Q", original_length_bits))
    return bytes(padded)

# ============================================================================
# PHẦN 2. LÕI MD5 — HÀM CHÍNH CỦA TOÀN BỘ CHƯƠNG TRÌNH
# ============================================================================




# ============================================================================
# PHẦN 3. TÍNH MD5 CHO TỆP VÀ KIỂM TRA TÍNH TOÀN VẸN
# ============================================================================





# ============================================================================
# PHẦN 4. TỰ KIỂM THỬ — GIỮ TEST CƠ BẢN TRONG MAIN.PY
# ============================================================================




# ============================================================================
# PHẦN 5. GIAO DIỆN DÒNG LỆNH (CLI) ĐỂ DEMO TRÊN CMD
# ============================================================================



