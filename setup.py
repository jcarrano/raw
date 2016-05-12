#!/usr/bin/env python

"""
setup.py file for RAW library
"""

from distutils.core import setup, Extension
from distutils.command.build_py import build_py as _build_py
from distutils import sysconfig, spawn
from distutils.version import LooseVersion
import subprocess, re

def get_swig_executable():
    "Get SWIG executable"

    # Find SWIG executable
    swig_executable = None
    swig_minimum_version = "3.0.3"
    for executable in ["swig", "swig3.0"]:
        swig_executable = spawn.find_executable(executable)
        if swig_executable is not None:
            # Check that SWIG version is ok
            output = subprocess.check_output([swig_executable, "-version"]).decode('utf-8')
            swig_version = re.findall(r"SWIG Version ([0-9.]+)", output)[0]
            if LooseVersion(swig_version) >= LooseVersion(swig_minimum_version):
                break
            swig_executable = None
    if swig_executable is None:
        raise OSError("Unable to find SWIG version %s or higher." % swig_minimum_version)
    print("Found SWIG: %s (version %s)" % (swig_executable, swig_version))

    return swig_executable


class Build_Ext_find_swig3(_build_py):
    def find_swig(self):
        return get_swig_executable()

libraw_wrapper = Extension('libraw',
                           sources=['libraw.i'],
                           swig_opts=['-builtin', '-lraw'],
                           )

setup (name = 'libraw',
       version = '0.1',
       author      = "Juan I Carrano",
       description = """LibRaw Wrapper""",
       ext_modules = [libraw_wrapper],
       py_modules = ["libraw"],
       cmdclass = {"build_ext": Build_Ext_find_swig3}
       )