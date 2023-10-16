from _typeshed import Incomplete
from conan.tools.apple.apple import is_apple_os as is_apple_os
from conan.tools.microsoft import is_msvc as is_msvc

class GnuDepsFlags:
    _conanfile: Incomplete
    _subsystem: Incomplete
    include_paths: Incomplete
    lib_paths: Incomplete
    defines: Incomplete
    libs: Incomplete
    frameworks: Incomplete
    framework_paths: Incomplete
    cxxflags: Incomplete
    cflags: Incomplete
    sharedlinkflags: Incomplete
    exelinkflags: Incomplete
    system_libs: Incomplete
    def __init__(self, conanfile, cpp_info) -> None: ...
    _GCC_LIKE: Incomplete
    @staticmethod
    def _format_defines(defines): ...
    def _format_frameworks(self, frameworks, is_path: bool = ...): ...
    def _format_include_paths(self, include_paths): ...
    def _format_library_paths(self, library_paths): ...
    def _format_libraries(self, libraries): ...
    def _adjust_path(self, path): ...
