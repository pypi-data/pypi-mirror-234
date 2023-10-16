from _typeshed import Incomplete
from conan.tools.build import cross_building as cross_building

class _SystemPackageManagerTool:
    mode_check: str
    mode_install: str
    tool_name: Incomplete
    install_command: str
    update_command: str
    check_command: str
    accepted_install_codes: Incomplete
    accepted_update_codes: Incomplete
    accepted_check_codes: Incomplete
    _conanfile: Incomplete
    _active_tool: Incomplete
    _sudo: Incomplete
    _sudo_askpass: Incomplete
    _mode: Incomplete
    _arch: Incomplete
    _arch_names: Incomplete
    _arch_separator: str
    def __init__(self, conanfile) -> None: ...
    def get_default_tool(self): ...
    def get_package_name(self, package): ...
    @property
    def sudo_str(self): ...
    def run(self, method, *args, **kwargs): ...
    def _conanfile_run(self, command, accepted_returns): ...
    def install_substitutes(self, *args, **kwargs): ...
    def install(self, *args, **kwargs): ...
    def update(self, *args, **kwargs): ...
    def check(self, *args, **kwargs): ...
    def _install_substitutes(self, *packages_substitutes, update: bool = ..., check: bool = ..., **kwargs): ...
    def _install(self, packages, update: bool = ..., check: bool = ..., **kwargs): ...
    def _update(self): ...
    def _check(self, packages): ...
    def check_package(self, package): ...

class Apt(_SystemPackageManagerTool):
    tool_name: str
    install_command: str
    update_command: str
    check_command: str
    _arch_names: Incomplete
    _arch_separator: str
    def __init__(self, conanfile, arch_names: Incomplete | None = ...) -> None: ...
    def install(self, packages, update: bool = ..., check: bool = ..., recommends: bool = ...): ...

class Yum(_SystemPackageManagerTool):
    tool_name: str
    install_command: str
    update_command: str
    check_command: str
    accepted_update_codes: Incomplete
    _arch_names: Incomplete
    _arch_separator: str
    def __init__(self, conanfile, arch_names: Incomplete | None = ...) -> None: ...

class Dnf(Yum):
    tool_name: str

class Brew(_SystemPackageManagerTool):
    tool_name: str
    install_command: str
    update_command: str
    check_command: str

class Pkg(_SystemPackageManagerTool):
    tool_name: str
    install_command: str
    update_command: str
    check_command: str

class PkgUtil(_SystemPackageManagerTool):
    tool_name: str
    install_command: str
    update_command: str
    check_command: str

class Chocolatey(_SystemPackageManagerTool):
    tool_name: str
    install_command: str
    update_command: str
    check_command: str

class PacMan(_SystemPackageManagerTool):
    tool_name: str
    install_command: str
    update_command: str
    check_command: str
    _arch_names: Incomplete
    _arch_separator: str
    def __init__(self, conanfile, arch_names: Incomplete | None = ...) -> None: ...

class Zypper(_SystemPackageManagerTool):
    tool_name: str
    install_command: str
    update_command: str
    check_command: str
