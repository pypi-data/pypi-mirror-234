from _typeshed import Incomplete

PREMAKE_FILE: str

class _PremakeTemplate:
    includedirs: Incomplete
    libdirs: Incomplete
    bindirs: Incomplete
    libs: Incomplete
    system_libs: Incomplete
    defines: Incomplete
    cxxflags: Incomplete
    cflags: Incomplete
    sharedlinkflags: Incomplete
    exelinkflags: Incomplete
    frameworks: Incomplete
    sysroot: Incomplete
    def __init__(self, deps_cpp_info) -> None: ...

class PremakeDeps:
    _conanfile: Incomplete
    def __init__(self, conanfile) -> None: ...
    def generate(self) -> None: ...
    def _get_cpp_info(self): ...
    @property
    def content(self): ...
