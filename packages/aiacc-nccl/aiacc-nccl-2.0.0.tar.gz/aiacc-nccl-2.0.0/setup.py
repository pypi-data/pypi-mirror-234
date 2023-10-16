#
# Copyright (C) Alibaba Cloud Ltd. 2021-2024.  ALL RIGHTS RESERVED.
#
import sys
import os
import shutil
import time
import platform

#import torch
#from torch.utils import cpp_extension
#from Cython.Build import cythonize
from setuptools import setup, Extension, find_packages
from wheel.bdist_wheel import bdist_wheel
from setuptools.command.build_ext import build_ext
from setuptools.command.install import install 
#from distutils.core import setup
#from distutils.command.install import install


aiacc_nccl_version = "2.0.0"
# package_name = "aiacc_nccl_cu11"
package_name = "aiacc-nccl"
total_packages = [
    "aiacc_nccl"
]

class post_install(install):
    def run(self):
        # print('install ...')
        install.run(self)
        path = os.__file__
        from distutils.sysconfig import get_python_lib
        #>>> get_python_lib()
        #'/root/miniconda3/lib/python3.9/site-packages'
        path = get_python_lib() + '/aiacc_nccl/'
        if os.path.exists('/etc/ld.so.conf.d/aiacc_nccl.conf'):
            os.system(f'echo {path} >> "/etc/ld.so.conf.d/aiacc_nccl.conf"')
        else:
            os.system(f'echo {path} > "/etc/ld.so.conf.d/aiacc_nccl.conf"')
        os.system(f'ldconfig')
        # print('echo aiacc_nccl install done!')

setup(
    name=package_name,
    version=f"{aiacc_nccl_version}",
    description=("AIACC-NCCL is an AI-Accelerator communication framework for NVIDIA-NCCL. "\
                 "It implements optimized all-reduce, all-gather, reduce, broadcast, reduce-scatter, all-to-all," \
                 "as well as any send/receive based communication pattern." \
                 "It has been optimized to achieve high bandwidth on aliyun machines using PCIe, NVLink, NVswitch," \
                 "as well as networking using InfiniBand Verbs, eRDMA or TCP/IP sockets."),
    author="Alibaba Cloud",
    author_email="ziqi.yzq@alibaba-inc.com",
    license="Copyright (C) Alibaba Group Holding Limited",
    keywords="Distributed, Deep Learning, Communication, NCCL, AIACC",
    url="https://help.aliyun.com/document_detail/462422.html?spm=a2c4g.462031.0.0.c5f96b4drcx52F",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    packages=total_packages,
    package_dir={package_name: "aiacc_nccl"},
    package_data={'aiacc_nccl': ['libnccl.so.2']},
    include_package_data=True,
    #data_files=[("aiacc_nccl", ["aiacc/aiacc.so"])],
    # ext_modules=aiacc_ext_modules,
    # scripts=['aiacc_bind'],
    # cmdclass=aiacc_cmdclass
    # install_requires=['aiacc_nccl_cu11']
    cmdclass={
      'install': post_install
    }
)
