#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2016 The CyanogenMod Project
# SPDX-FileCopyrightText: 2017-2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.file import File
from extract_utils.fixups_blob import (
    BlobFixupCtx,
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/xiaomi/miuicamera-rubyx',
]

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}-{partition}' if partition == 'vendor' else None

blob_fixups: blob_fixups_user_type = {
    'system_ext/lib64/libcamera_algoup_jni.xiaomi.so': blob_fixup()
            .add_needed('libgui_shim_miuicamera.so')
	    .sig_replace('08 AD 40 F9', '08 A9 40 F9'),
    ('system_ext/lib64/libcamera_mianode_jni.xiaomi.so',
     'system_ext/lib64/libcamera_ispinterface_jni.xiaomi.so'): blob_fixup()
            .add_needed('libgui_shim_miuicamera.so'),
            
    'system_ext/lib64/vendor.mediatek.hardware.camera.isphal-V1-ndk.so': blob_fixup()
        .replace_needed('android.hardware.graphics.common-V5-ndk.so','android.hardware.graphics.common-V6-ndk.so'),
        
    'system_ext/priv-app/MiuiCamera/MiuiCamera.apk': blob_fixup()
        .apktool_patch('patches/MIUICamera.patch'),
}

module = ExtractUtilsModule(
    'miuicamera-rubyx',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    add_firmware_proprietary_file=False,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
