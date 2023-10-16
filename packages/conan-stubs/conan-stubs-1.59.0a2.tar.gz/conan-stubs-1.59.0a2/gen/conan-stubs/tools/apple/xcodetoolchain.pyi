from _typeshed import Incomplete
from conan.tools._check_build_profile import check_using_build_profile as check_using_build_profile
from conan.tools._compilers import cppstd_flag as cppstd_flag
from conan.tools.apple import to_apple_arch as to_apple_arch
from conan.tools.apple.xcodedeps import GLOBAL_XCCONFIG_FILENAME as GLOBAL_XCCONFIG_FILENAME, GLOBAL_XCCONFIG_TEMPLATE as GLOBAL_XCCONFIG_TEMPLATE, _add_includes_to_file_or_create as _add_includes_to_file_or_create, _xcconfig_conditional as _xcconfig_conditional, _xcconfig_settings_filename as _xcconfig_settings_filename

class XcodeToolchain:
    filename: str
    extension: str
    _vars_xconfig: Incomplete
    _flags_xconfig: Incomplete
    _agreggated_xconfig: Incomplete
    _conanfile: Incomplete
    architecture: Incomplete
    configuration: Incomplete
    sdk: Incomplete
    sdk_version: Incomplete
    libcxx: Incomplete
    os_version: Incomplete
    _global_defines: Incomplete
    _global_cxxflags: Incomplete
    _global_cflags: Incomplete
    _global_ldflags: Incomplete
    def __init__(self, conanfile) -> None: ...
    def generate(self) -> None: ...
    @property
    def _cppstd(self): ...
    @property
    def _macosx_deployment_target(self): ...
    @property
    def _clang_cxx_library(self): ...
    @property
    def _clang_cxx_language_standard(self): ...
    @property
    def _vars_xconfig_filename(self): ...
    @property
    def _vars_xconfig_content(self): ...
    @property
    def _agreggated_xconfig_content(self): ...
    @property
    def _global_xconfig_content(self): ...
    @property
    def _agreggated_xconfig_filename(self): ...
    @property
    def _check_if_extra_flags(self): ...
    @property
    def _flags_xcconfig_content(self): ...
    @property
    def _flags_xcconfig_filename(self): ...
