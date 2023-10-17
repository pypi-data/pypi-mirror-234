import os
import platform


this_dir = os.path.dirname(os.path.abspath(__file__))
_plfm = platform.machine()
arch = "amd64" if _plfm == "x86_64" else "arm64" if _plfm == "aarch64" else "armhf"
arch_dir = os.path.join(this_dir, arch)

try:
    from ...__config__ import LIBTIEPIE as DLL_PATH
except ImportError:
    DLL_PATH = os.path.join(arch_dir, 'libtiepie-hw.so.1')
