from _typeshed import Incomplete
from conan.tools._check_build_profile import check_using_build_profile as check_using_build_profile
from conan.tools.cmake.cmakedeps import FIND_MODE_BOTH as FIND_MODE_BOTH, FIND_MODE_CONFIG as FIND_MODE_CONFIG, FIND_MODE_MODULE as FIND_MODE_MODULE, FIND_MODE_NONE as FIND_MODE_NONE
from conan.tools.cmake.cmakedeps.templates.config import ConfigTemplate as ConfigTemplate
from conan.tools.cmake.cmakedeps.templates.config_version import ConfigVersionTemplate as ConfigVersionTemplate
from conan.tools.cmake.cmakedeps.templates.macros import MacrosTemplate as MacrosTemplate
from conan.tools.cmake.cmakedeps.templates.target_configuration import TargetConfigurationTemplate as TargetConfigurationTemplate
from conan.tools.cmake.cmakedeps.templates.target_data import ConfigDataTemplate as ConfigDataTemplate
from conan.tools.cmake.cmakedeps.templates.targets import TargetsTemplate as TargetsTemplate

class CMakeDeps:
    _conanfile: Incomplete
    arch: Incomplete
    configuration: Incomplete
    build_context_activated: Incomplete
    build_context_build_modules: Incomplete
    build_context_suffix: Incomplete
    check_components_exist: bool
    _properties: Incomplete
    def __init__(self, conanfile) -> None: ...
    def generate(self) -> None: ...
    @property
    def content(self): ...
    def _generate_files(self, require, dep, ret, find_module_mode) -> None: ...
    def set_property(self, dep, prop, value, build_context: bool = ...) -> None: ...
    def get_property(self, prop, dep, comp_name: Incomplete | None = ...): ...
    def get_cmake_package_name(self, dep, module_mode: Incomplete | None = ...): ...
    def get_find_mode(self, dep): ...
