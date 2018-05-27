#!/usr/bin/env python3

import argparse
import subprocess
import shutil
import os

from pathlib import Path

sdk_path = Path(os.environ['ANDROID_SDK_ROOT']).resolve()
ndk_path = (sdk_path / 'ndk-bundle').resolve()

root_path = Path(__file__).parent.resolve()
build_path = root_path / 'distribution'


def get_cmake_path():
    cmake_variants = [v for v in (sdk_path / 'cmake').iterdir() if v.is_dir()]
    if len(cmake_variants) == 0:
        exit(-1)
    
    return (sorted(cmake_variants)[-1]).resolve()


def build():
    cmd_build = [str(get_cmake_path() / 'bin' / 'cmake'), '--build', '.']
    subprocess.run(cmd_build, check=True)


def generate():
    cmd = [
           str(get_cmake_path() / 'bin' / 'cmake'),
           '-G', 'Ninja',
           '-DCMAKE_MAKE_PROGRAM=%s' % str(get_cmake_path() / 'bin' / 'ninja'),
           '-DANDROID_ABI=arm64-v8a',
           '-DCMAKE_BUILD_TYPE=Release',
           '-DCMAKE_TOOLCHAIN_FILE=%s' % str(ndk_path / 'build' / 'cmake' / 'android.toolchain.cmake'),
           '-DANDROID_PLATFORM=android-27',
           '-DANDROID_ARM_NEON=TRUE',
           '-DANDROID_TOOLCHAIN=clang',
           '-DANDROID_NATIVE_API_LEVEL=27',
           '-DANDROID_STL=c++_static',
           '-DANDROID_CPP_FEATURES=rtti exceptions',
           '-DBUILD_ANDROID_PROJECTS=0',
           str(root_path)  # source dir
           ]
    subprocess.run(cmd, check=True)


def prepare():
    build_path.mkdir(parents=True, exist_ok=True)


def clean():
    shutil.rmtree(build_path, ignore_errors=True)


def main():
    clean()
    prepare()
    os.chdir(str(build_path))
    generate()
    build()


if __name__ == '__main__':
    main()

