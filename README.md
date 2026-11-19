# device/meizu/m2381-kernel

Prebuilt kernel inputs for Meizu 20 (`m2381`).

| Path | Purpose |
| ---- | ------- |
| `Image` | Stock kernel binary, Linux 5.15 |
| `dtb.img` | Merged DTB for `vendor_boot.img` |
| `dtb/m2381.dtb` | Device tree blob, unpacked from stock |
| `dtb/android/m2381.dtb` | Android adaptation that selects the ramdisk fstab |
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

## Android 分区挂载

原厂 DTB 的 `/firmware/android/fstab` 指向旧 ext4 vendor 分区。独立的
`dtb/android/m2381.dtb` 仅把这个节点的 `status` 设为 `disabled`，让 init 使用
ramdisk 内的 EROFS/逻辑分区 fstab。原始 `dtb/m2381.dtb` 保持不变。

使用 AOSP checkout 自带的 libfdt 复现兼容副本并核验固定输入/输出摘要：

```bash
python3 tools/prepare_android_dtb.py --aosp /path/to/android --apply
python3 tools/prepare_android_dtb.py --aosp /path/to/android
```

未知输入或未知的已有输出会被拒绝；不改硬件节点、CPU idle 或启动脚本。

## 上游预编译头接口

kernel-headers.tar.gz 由设备 BoardConfig 的 TARGET_PREBUILT_KERNEL_HEADERS 选择，不修改全局 generated_kernel_includes。tools/package_build_headers.py --aosp AOSP_ROOT 可复现该有限编译输入；它包含已有 msm_audio.h 和清理工具要求的通用头，不是完整原厂 UAPI，不能用于启用源码 QTI HAL。
