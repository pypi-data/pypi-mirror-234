from _typeshed import Incomplete
from conan.tools.apple import to_apple_arch as to_apple_arch

class XcodeBuild:
    _conanfile: Incomplete
    _build_type: Incomplete
    _arch: Incomplete
    _sdk: Incomplete
    _sdk_version: Incomplete
    def __init__(self, conanfile) -> None: ...
    @property
    def _verbosity(self): ...
    @property
    def _sdkroot(self): ...
    def build(self, xcodeproj, target: Incomplete | None = ...) -> None: ...
