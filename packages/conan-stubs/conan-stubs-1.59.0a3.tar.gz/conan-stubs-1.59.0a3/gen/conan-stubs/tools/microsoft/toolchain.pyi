from _typeshed import Incomplete
from conan.tools._check_build_profile import check_using_build_profile as check_using_build_profile
from conan.tools.build import build_jobs as build_jobs
from conan.tools.intel.intel_cc import IntelCC as IntelCC
from conan.tools.microsoft.visual import VCVars as VCVars, msvs_toolset as msvs_toolset

class MSBuildToolchain:
    filename: str
    _config_toolchain_props: Incomplete
    _conanfile: Incomplete
    preprocessor_definitions: Incomplete
    compile_options: Incomplete
    cxxflags: Incomplete
    cflags: Incomplete
    ldflags: Incomplete
    configuration: Incomplete
    runtime_library: Incomplete
    cppstd: Incomplete
    toolset: Incomplete
    properties: Incomplete
    def __init__(self, conanfile) -> None: ...
    def _name_condition(self, settings): ...
    def generate(self) -> None: ...
    @staticmethod
    def _runtime_library(settings): ...
    @property
    def context_config_toolchain(self): ...
    def _write_config_toolchain(self, config_filename) -> None: ...
    def _write_main_toolchain(self, config_filename, condition) -> None: ...
    def _get_extra_flags(self): ...
