from _typeshed import Incomplete
from conan.tools.cmake.cmakedeps import FIND_MODE_BOTH as FIND_MODE_BOTH, FIND_MODE_CONFIG as FIND_MODE_CONFIG, FIND_MODE_MODULE as FIND_MODE_MODULE, FIND_MODE_NONE as FIND_MODE_NONE
from conan.tools.cmake.cmakedeps.templates import CMakeDepsFileTemplate as CMakeDepsFileTemplate

class ConfigDataTemplate(CMakeDepsFileTemplate):
    @property
    def filename(self): ...
    @property
    def context(self): ...
    @property
    def template(self): ...
    def _get_global_cpp_cmake(self): ...
    @property
    def _root_folder(self): ...
    def _get_required_components_cpp(self): ...
    def _get_dependency_filenames(self): ...
    def _get_dependencies_find_modes(self): ...

class _TargetDataContext:
    include_paths: Incomplete
    lib_paths: Incomplete
    res_paths: Incomplete
    bin_paths: Incomplete
    build_paths: Incomplete
    src_paths: Incomplete
    framework_paths: Incomplete
    libs: Incomplete
    system_libs: Incomplete
    frameworks: Incomplete
    defines: Incomplete
    compile_definitions: Incomplete
    cxxflags_list: Incomplete
    cflags_list: Incomplete
    sharedlinkflags_list: Incomplete
    exelinkflags_list: Incomplete
    objects_list: Incomplete
    build_modules_paths: Incomplete
    def __init__(self, cpp_info, pfolder_var_name, package_folder) -> None: ...
