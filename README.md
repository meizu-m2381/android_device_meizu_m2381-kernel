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
