from _typeshed import Incomplete

def _is_using_intel_oneapi(compiler_version): ...

class IntelCC:
    filename: str
    _conanfile: Incomplete
    _settings: Incomplete
    _compiler_version: Incomplete
    _mode: Incomplete
    _out: Incomplete
    arch: Incomplete
    def __init__(self, conanfile) -> None: ...
    @property
    def ms_toolset(self): ...
    def generate(self, scope: str = ...) -> None: ...
    @property
    def installation_path(self): ...
    @property
    def command(self): ...
