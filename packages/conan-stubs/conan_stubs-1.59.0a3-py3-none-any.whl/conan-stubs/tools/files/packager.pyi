from _typeshed import Incomplete

class _PatternEntry:
    include: Incomplete
    lib: Incomplete
    bin: Incomplete
    src: Incomplete
    build: Incomplete
    res: Incomplete
    framework: Incomplete
    def __init__(self) -> None: ...

class _Patterns:
    source: Incomplete
    build: Incomplete
    def __init__(self) -> None: ...

class AutoPackager:
    _conanfile: Incomplete
    patterns: Incomplete
    def __init__(self, conanfile) -> None: ...
    def run(self) -> None: ...
    def _package_cppinfo(self, origin_name, origin_cppinfo, dest_cppinfo) -> None: ...
