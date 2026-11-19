#!/usr/bin/env python3
"""Reproduce the M2381 DTB that delegates mounting to the ramdisk fstab."""
import argparse
import ctypes
import hashlib
from pathlib import Path

STOCK_SHA256 = '58bb73795cb945f05de434b4abeecbe8c510069e7b45ce7afc598eb6e3d58671'
ANDROID_SHA256 = '31ca1ad17cd572f5971be1a702a29958e72f6f149d9bdbca71ac268e24093f2c'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--aosp', type=Path, required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    source = (root / 'dtb/m2381.dtb').read_bytes()
    if hashlib.sha256(source).hexdigest() != STOCK_SHA256:
        raise ValueError('Unknown stock DTB; refusing to modify it')
    output = root / 'dtb/android/m2381.dtb'
    if args.apply:
        lib = args.aosp / 'prebuilts/kernel-build-tools/linux-x86/lib64/libfdt.so'
        fdt = ctypes.CDLL(str(lib.resolve()))
        fdt.fdt_check_header.argtypes = [ctypes.c_void_p]
        fdt.fdt_open_into.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int]
        fdt.fdt_path_offset.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        fdt.fdt_setprop.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p,
                                  ctypes.c_void_p, ctypes.c_int]
        fdt.fdt_pack.argtypes = [ctypes.c_void_p]
        original = ctypes.create_string_buffer(source)
        buffer = ctypes.create_string_buffer(len(source) + 4096)
        if fdt.fdt_check_header(original) or fdt.fdt_open_into(original, buffer, len(buffer)):
            raise ValueError('Invalid stock DTB')
        node = fdt.fdt_path_offset(buffer, b'/firmware/android/fstab')
        if node < 0 or fdt.fdt_setprop(buffer, node, b'status', b'disabled\0', 9):
            raise ValueError('Cannot disable legacy DT fstab')
        if fdt.fdt_pack(buffer):
            raise ValueError('Cannot pack DTB')
        data = buffer.raw[:int.from_bytes(buffer.raw[4:8], 'big')]
        if hashlib.sha256(data).hexdigest() != ANDROID_SHA256:
            raise ValueError('Generated DTB differs from the verified adaptation')
        if output.exists() and hashlib.sha256(output.read_bytes()).hexdigest() != ANDROID_SHA256:
            raise ValueError('Refusing to overwrite an unknown Android DTB')
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(data)
    if hashlib.sha256(output.read_bytes()).hexdigest() != ANDROID_SHA256:
        raise ValueError('Android DTB is missing or has the wrong digest')
    print('M2381 Android DTB verified:', ANDROID_SHA256)


if __name__ == '__main__':
    main()
