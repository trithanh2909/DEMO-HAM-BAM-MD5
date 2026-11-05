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

_SHIFT = (
    [7, 12, 17, 22] * 4
    + [5, 9, 14, 20] * 4
    + [4, 11, 16, 23] * 4
    + [6, 10, 15, 21] * 4
)

_K = [int(abs(math.sin(i + 1)) * (1 << 32)) & _MASK32 for i in range(64)]

_INITIAL_STATE = (0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476)


def _left_rotate(value: int, amount: int) -> int:
    value &= _MASK32
    return ((value << amount) | (value >> (32 - amount))) & _MASK32


def _pad(message: bytes) -> bytes:
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
def md5(
    message: bytes,
    *,
    trace: bool = False, 
) -> str | tuple[str, list[dict[str, Any]]]:
    if not isinstance(message, (bytes, bytearray, memoryview)):
        raise TypeError("md5() cần bytes; hãy mã hóa văn bản bằng UTF-8 trước.")
    
    data = _pad(bytes(message))
    a0, b0, c0, d0 = _INITIAL_STATE 
    trace_rows: list[dict[str, Any]] = []
    
    for block_index in range(0, len(data), 64):
        block = data[block_index:block_index + 64]
        words = struct.unpack("<16I", block)
        a, b, c, d = a0, b0, c0, d0
        
        for i in range(64):
            if i < 16:
                function = (b & c) | ((~b) & d)
                word_index = i
                round_number = 1
            elif i < 32:
                function = (d & b) | ((~d) & c)
                word_index = (5 * i + 1) % 16
                round_number = 2  
            elif i < 48:
                function = b ^ c ^ d
                word_index = (3 * i + 5) % 16
                round_number = 3
            else:
                function = c ^ (b | (~d))
                word_index = (7 * i) % 16
                round_number = 4
                
            mixed = (a + function + _K[i] + words[word_index]) & _MASK32
            rotated = _left_rotate(mixed, _SHIFT[i]) 
                
            old_b, old_c, old_d = b, c, d
            a = old_d
            b = (old_b + rotated) & _MASK32
            c = old_b
            d = old_c
                
            if trace:
                trace_rows.append(
                    {
                        "block": block_index // 64 + 1,
                        "step": i + 1,
                        "round": round_number,
                        "word_index": word_index,
                        "A": f"{a:08x}",
                        "B": f"{b:08x}",
                        "C": f"{c:08x}",
                        "D": f"{d:08x}",
                    }
                )
                    
        a0 = (a0 + a) & _MASK32
        b0 = (b0 + b) & _MASK32
        c0 = (c0 + c) & _MASK32
        d0 = (d0 + d) & _MASK32
        
    digest_bytes = struct.pack("<4I", a0, b0, c0, d0)
    digest = digest_bytes.hex()
    return (digest, trace_rows) if trace else digest

def md5_text(text: str) -> str:
    return str(md5(text.encode("utf-8")))
    

# ============================================================================
# PHẦN 3. TÍNH MD5 CHO TỆP VÀ KIỂM TRA TÍNH TOÀN VẸN
# ============================================================================
def hash_file(path: str | Path) -> str:
    file_path = Path(path).expanduser()
    data = file_path.read_bytes()
    return str(md5(data))

def verify_file(path: str | Path, expected_digest: str) -> tuple[bool, str]:
    actual = hash_file(path)
    normalized = expected_digest.strip().lower()
    is_valid_digest = len(normalized) == 32 and all(
        char in "0123456789abcdef" for char in normalized
    )
    matched = is_valid_digest and hmac.compare_digest(actual, normalized)
    return matched, actual
    
# ============================================================================
# PHẦN 4. TỰ KIỂM THỬ — GIỮ TEST CƠ BẢN TRONG MAIN.PY
# ============================================================================
def self_test() -> bool:
    vectors = [
        (b"", "d41d8cd98f00b204e9800998ecf8427e"),
        (b"a", "0cc175b9c0f1b6a831c399e269772661"),
        (b"abc", "900150983cd24fb0d6963f7d28e17f72"),
        (b"message digest", "f96b697d7cb7938d525a2f31aaf161d0"),
        (b"abcdefghijklmnopqrstuvwxyz", "c3fcd3d76192e4007dfb496cca67e13b"),
        (
            b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
            "d174ab98d277d9f5a5611c2c9f419d9f",
        ),
        (b"1234567890 * 8, "57edf4a22be3c955ac49da2e2107b67a"),
    ]

    total = 0
    passed = 0

    def check(name: str, condition: bool) -> None:
        nonlocal total, passed
        total += 1
        if condition:
            passed += 1
            print(f"[PASS] {name}")
        else:
            print(f"[FAIL] {name}")
    print("\n========== TỰ KIỂM THỬ MD5 ==========")
    for index, (message, expected) in enumerate(vectors, start=1):
        check(f"RFC 1321 test vector {index}", md5(message) == expected)

    boundary_ok = True
    for length in (0, 1, 55, 56, 63, 64, 65, 127, 128, 129, 1024):
        data = bytes(i % 256 for i in range(length))
        if md5(data) != hashlib.md5(data).hexdigest():
            boundary_ok = False
            break
    check("Độ dài biên padding và khối dữ liệu", boundary_ok)

    unicode_ok = md5_text("Xin chào Việt Nam") == hashlib.md5(
        "Xin chào Việt Nam".encode("utf-8")
    ).hexdigest()
    check("Văn bản tiếng Việt UTF-8", unicode_ok)   

     try:
        md5("abc")  # type: ignore[arg-type]
        type_ok = False
    except TypeError:
        type_ok = True
    check("Từ chối đầu vào chuỗi chưa mã hóa thành bytes", type_ok)

    trace_result = md5(b"abc", trace=True)
    trace_ok = (
        isinstance(trace_result, tuple)
        and trace_result[0] == "900150983cd24fb0d6963f7d28e17f72"
        and len(trace_result[1]) == 64
    )
    check("Trace có đủ 64 bước cho khối abc", trace_ok)

    with tempfile.TemporaryDirectory() as directory:
        sample = Path(directory) / "sample.txt"
        sample.write_bytes(b"MD5 integrity test")
        original_digest = hash_file(sample)
        match_ok = verify_file(sample, original_digest.upper())[0]
        check("Tệp nguyên bản khớp digest tham chiếu", match_ok)

        sample.write_bytes(b"MD5 integrity test changed")
        mismatch_ok = not verify_file(sample, original_digest)[0]
        check("Tệp thay đổi không khớp digest cũ", mismatch_ok)

        invalid_ok = not verify_file(sample, "not-a-digest")[0]
        check("Từ chối digest sai định dạng", invalid_ok)

    print(f"\nKết quả: {passed}/{total} kiểm tra đạt.")
    print("OK" if passed == total else "CÓ KIỂM TRA THẤT BẠI")
    return passed == total    



# ============================================================================
# PHẦN 5. GIAO DIỆN DÒNG LỆNH (CLI) ĐỂ DEMO TRÊN CMD
# ============================================================================



