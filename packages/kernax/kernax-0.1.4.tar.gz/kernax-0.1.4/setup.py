# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.

import os
import re
from setuptools import setup

VERSIONFILE="kernax/_version.py"
if os.path.isfile(VERSIONFILE):
    verstrline = open(VERSIONFILE, "rt").read()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        verstr = mo.group(1)
    else:
        raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))
else:
    verstr = "1.0"

setup(
    name="kernax",
    version=verstr,
    packages=["kernax"],
    description="Kernelized Stein discrepancy thinning",
    author="Brian Staber",
    author_email="brian.staber@safrangroup.com",
    include_package_data=True
)
