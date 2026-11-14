/*
 * M2381 专用：msm_audio.h 的重建版本，仅用于编译通过。
 *
 * 背景：hardware/qcom-caf/sm8550/audio/graphservices 的 ar_osal 依赖
 * <linux/msm_audio.h>，该头文件属于高通内核 uapi，魅族未公开 m2381 内核源码，
 * AOSP 树内也没有副本。
 *
 * 使用范围：只被 AR_OSAL（音频 shared memory 抽象层）引用，而本机的音频 HAL
 * 实际由 vendor blobs 提供（android.hardware.audio.service_64，以及 libagm 与
 * libpal 系列库），这里编出来的 liblx-osal 不会进入最终镜像。
 *
 * 因此本文件只保证编译期类型正确，ioctl 编号按 msm_audio_ion 驱动的通行定义填写，
 * 未做运行时验证。若将来改为源码音频栈，必须替换为内核里的真实头文件。
 */
#ifndef _UAPI_LINUX_MSM_AUDIO_H
#define _UAPI_LINUX_MSM_AUDIO_H

#include <linux/types.h>
#include <linux/ioctl.h>

/* 物理地址映射（参数为 uint32 的 fd/handle） */
#define IOCTL_MAP_PHYS_ADDR     _IOW('A', 102, __u32)
#define IOCTL_UNMAP_PHYS_ADDR   _IOW('A', 103, __u32)

/* 虚拟机内存分配映射 */
#define IOCTL_MAP_HYP_ASSIGN    _IOW('A', 104, __u32)
#define IOCTL_UNMAP_HYP_ASSIGN  _IOW('A', 105, __u32)

#endif /* _UAPI_LINUX_MSM_AUDIO_H */
