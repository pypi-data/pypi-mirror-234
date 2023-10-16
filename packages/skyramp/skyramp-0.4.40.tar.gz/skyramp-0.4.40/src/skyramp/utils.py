"""
Contains internal utilities
"""

import platform
import os
import ctypes

SKYRAMP_YAML_VERSION = "v1"

def _get_c_library():
    system = platform.system().lower()
    machine = platform.machine().lower()

    lib_dir = os.path.join(os.path.dirname(__file__), "lib")
    lib_file = ""

    if system == "darwin":
        if machine == "arm64":
            lib_file = "dev-darwin-arm64.dylib"
    elif system == "linux":
        if machine in ["amd64", "x86_64"]:
            lib_file = "dev-linux-amd64.so"

    if lib_file == "":
        raise Exception(
            f"unsupported system and architecture. System: {system}, Architecture: {machine}"
        )

    lib_path = os.path.join(lib_dir, lib_file)

    return ctypes.cdll.LoadLibrary(lib_path)

def _call_function(func, argtypes, restype, args, return_output=False):
    func.argtypes = argtypes
    func.restype = restype

    output = func(*args)
    if not output:
        return None

    output_bytes = ctypes.string_at(output)
    output = output_bytes.decode()

    if return_output:
        return output

    # If output is not expected, the result output is parsed as an exception
    if len(output) > 0:
        raise Exception(output)

    return None


_library = _get_c_library()

if _library is None:
    raise Exception("failed to load Skyramp C library")
