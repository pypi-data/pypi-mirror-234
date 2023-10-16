from _typeshed import Incomplete

_profile_name: str
_profiles_prefix_in_config: Incomplete
_architecture: Incomplete
_build_variant: Incomplete
_optimization: Incomplete
_cxx_language_version: Incomplete
_target_platform: Incomplete
_runtime_library: Incomplete

def _bool(b): ...
def _env_var_to_list(var): ...
def _check_for_compiler(conanfile) -> None: ...
def _default_compiler_name(conanfile): ...
def _settings_dir(conanfile): ...
def _setup_toolchains(conanfile) -> None: ...
def _read_qbs_toolchain_from_config(conanfile): ...

class LinkerFlagsParser:
    driver_linker_flags: Incomplete
    linker_flags: Incomplete
    def __init__(self, ld_flags) -> None: ...

def _flags_from_env(): ...

class QbsProfile:
    filename: str
    old_filename: str
    _template_toolchain: Incomplete
    _conanfile: Incomplete
    _profile_values_from_setup: Incomplete
    _profile_values_from_env: Incomplete
    _architecture: Incomplete
    _build_variant: Incomplete
    _optimization: Incomplete
    _cxx_language_version: Incomplete
    _target_platform: Incomplete
    _runtime_library: Incomplete
    _sysroot: Incomplete
    _position_independent_code: Incomplete
    def __init__(self, conanfile) -> None: ...
    def generate(self) -> None: ...
    @property
    def content(self): ...
