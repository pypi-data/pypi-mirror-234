# Copyright (c) 2019-2021 CRS4
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
pyvqnet init
"""
from .version import VERSION
from . import nn, optim, qnn, tensor, utils, data, _core, dtype, device
from .utils import compare_torch_result
from .dtype import kbool, kcomplex128, kcomplex64, kfloat32, kfloat64, \
    kint16, kint32, kint64, kint8, kuint8

from .device import DEV_CPU
from .device import DEV_GPU_0
from .device import DEV_GPU_1
from .device import DEV_GPU_2
from .device import DEV_GPU_3
from .device import DEV_GPU_4
from .device import DEV_GPU_5
from .device import DEV_GPU_6
from .device import DEV_GPU_7
from .device import if_gpu_compiled
__version__ = VERSION
