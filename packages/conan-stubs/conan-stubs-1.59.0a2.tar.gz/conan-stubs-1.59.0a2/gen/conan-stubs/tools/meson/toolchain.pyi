from conan.tools.meson.helpers import *
from _typeshed import Incomplete
from conan.tools._check_build_profile import check_using_build_profile as check_using_build_profile
from conan.tools._compilers import libcxx_flags as libcxx_flags
from conan.tools.apple.apple import apple_min_version_flag as apple_min_version_flag, apple_sdk_path as apple_sdk_path, is_apple_os as is_apple_os, to_apple_arch as to_apple_arch
from conan.tools.build.cross_building import cross_building as cross_building, get_cross_building_settings as get_cross_building_settings
from conan.tools.env import VirtualBuildEnv as VirtualBuildEnv
from conan.tools.microsoft import VCVars as VCVars, msvc_runtime_flag as msvc_runtime_flag

class MesonToolchain:
    native_filename: str
    cross_filename: str
    _meson_file_template: Incomplete
    _conanfile: Incomplete
    _os: Incomplete
    _is_apple_system: Incomplete
    _backend: Incomplete
    _buildtype: Incomplete
    _b_ndebug: Incomplete
    _b_staticpic: Incomplete
    _default_library: Incomplete
    _cpp_std: Incomplete
    _b_vscrt: Incomplete
    properties: Incomplete
    project_options: Incomplete
    preprocessor_definitions: Incomplete
    pkg_config_path: Incomplete
    cross_build: Incomplete
    c: Incomplete
    cpp: Incomplete
    c_ld: Incomplete
    cpp_ld: Incomplete
    ar: Incomplete
    strip: Incomplete
    as_: Incomplete
    windres: Incomplete
    pkgconfig: Incomplete
    c_args: Incomplete
    c_link_args: Incomplete
    cpp_args: Incomplete
    cpp_link_args: Incomplete
    apple_arch_flag: Incomplete
    apple_isysroot_flag: Incomplete
    apple_min_version_flag: Incomplete
    objc: Incomplete
    objcpp: Incomplete
    objc_args: Incomplete
    objc_link_args: Incomplete
    objcpp_args: Incomplete
    objcpp_link_args: Incomplete
    def __init__(self, conanfile, backend: Incomplete | None = ...) -> None: ...
    def _get_default_dirs(self): ...
    def _resolve_apple_flags_and_variables(self, build_env, compilers_by_conf) -> None: ...
    def _resolve_android_cross_compilation(self) -> None: ...
    def _get_extra_flags(self): ...
    @staticmethod
    def _get_env_list(v): ...
    @staticmethod
    def _filter_list_empty_fields(v): ...
    def _context(self): ...
    @property
    def content(self): ...
    def generate(self) -> None: ...
