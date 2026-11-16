#!/usr/bin/env python3
"""Reproduce the limited, build-only archive for Lineage's prebuilt header API.

The three sanitized generic headers are from the pinned Android 17 bionic
checkout. msm_audio.h remains the historical compatibility definition; this
archive is not a complete Meizu kernel UAPI and must not enable source QTI HALs.
"""
import argparse
import gzip
import io
from pathlib import Path
import tarfile

ROOT = Path(__file__).resolve().parents[1]


def package(aosp):
    sources = {
        'usr/include/asm/signal.h': aosp / 'bionic/libc/kernel/uapi/asm-arm64/asm/signal.h',
        'usr/include/asm-generic/signal.h': aosp / 'bionic/libc/kernel/uapi/asm-generic/signal.h',
        'usr/include/linux/eventpoll.h': aosp / 'bionic/libc/kernel/uapi/linux/eventpoll.h',
        'usr/include/linux/msm_audio.h': ROOT / 'include/linux/msm_audio.h',
    }
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode='w', format=tarfile.USTAR_FORMAT) as archive:
        for name, path in sorted(sources.items()):
            data = path.read_bytes().replace(b'\r\n', b'\n')
            entry = tarfile.TarInfo(name)
            entry.size, entry.mode = len(data), 0o644
            archive.addfile(entry, io.BytesIO(data))
    return gzip.compress(buffer.getvalue(), mtime=0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--aosp', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=ROOT / 'kernel-headers.tar.gz')
    args = parser.parse_args()
    args.output.write_bytes(package(args.aosp))
