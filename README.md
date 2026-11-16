# device/meizu/m2381-kernel

Prebuilt kernel inputs for Meizu 20 (`m2381`).

| Path | Purpose |
| ---- | ------- |
| `Image` | Stock kernel binary, Linux 5.15 |
| `dtb.img` | Merged DTB for `vendor_boot.img` |
| `dtb/m2381.dtb` | Device tree blob, unpacked from stock |
| `include/linux/msm_audio.h` | Build-only compatibility header |

## Notes

The Meizu kernel source and DTS for `m2381` are not published. The DT/config in
`meizu-sm8550-kernel` covers `m2468` only, so this tree ships the stock binary
instead of a source build. `BoardConfig.mk` selects it through
`TARGET_PREBUILT_KERNEL`.

## Retrieve

```bash
git lfs install
git lfs pull
```

`Image`, `dtb.img` and `dtb/**` are stored in Git LFS and total about 48 MB.

## Limitations

The prebuilt kernel does not ship a full UAPI header tree. `linux/msm_audio.h`
here exists only to satisfy build-time includes and is not a runtime ABI
contract.

## 上游预编译头接口

kernel-headers.tar.gz 由设备 BoardConfig 的 TARGET_PREBUILT_KERNEL_HEADERS 选择，不修改全局 generated_kernel_includes。tools/package_build_headers.py --aosp AOSP_ROOT 可复现该有限编译输入；它包含已有 msm_audio.h 和清理工具要求的通用头，不是完整原厂 UAPI，不能用于启用源码 QTI HAL。
