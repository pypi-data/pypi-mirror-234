from _typeshed import Incomplete
from collections import OrderedDict
from conan.tools._check_build_profile import check_using_build_profile as check_using_build_profile
from conan.tools._compilers import use_win_mingw as use_win_mingw
from conan.tools.cmake.presets import write_cmake_presets as write_cmake_presets
from conan.tools.cmake.toolchain import CONAN_TOOLCHAIN_FILENAME as CONAN_TOOLCHAIN_FILENAME
from conan.tools.cmake.toolchain.blocks import AndroidSystemBlock as AndroidSystemBlock, AppleSystemBlock as AppleSystemBlock, ArchitectureBlock as ArchitectureBlock, CMakeFlagsInitBlock as CMakeFlagsInitBlock, CompilersBlock as CompilersBlock, CppStdBlock as CppStdBlock, ExtraFlagsBlock as ExtraFlagsBlock, FPicBlock as FPicBlock, FindFiles as FindFiles, GLibCXXBlock as GLibCXXBlock, GenericSystemBlock as GenericSystemBlock, LinkerScriptsBlock as LinkerScriptsBlock, OutputDirsBlock as OutputDirsBlock, ParallelBlock as ParallelBlock, PkgConfigBlock as PkgConfigBlock, SharedLibBock as SharedLibBock, SkipRPath as SkipRPath, ToolchainBlocks as ToolchainBlocks, TryCompileBlock as TryCompileBlock, UserToolchain as UserToolchain, VSRuntimeBlock as VSRuntimeBlock
from conan.tools.intel import IntelCC as IntelCC
from conan.tools.microsoft import VCVars as VCVars
from conan.tools.microsoft.visual import vs_ide_version as vs_ide_version

class Variables(OrderedDict):
    _configuration_types: Incomplete
    def __init__(self) -> None: ...
    def __getattribute__(self, config): ...
    @property
    def configuration_types(self): ...
    def quote_preprocessor_strings(self) -> None: ...

class CMakeToolchain:
    filename = CONAN_TOOLCHAIN_FILENAME
    _template: Incomplete
    _conanfile: Incomplete
    generator: Incomplete
    variables: Incomplete
    cache_variables: Incomplete
    preprocessor_definitions: Incomplete
    blocks: Incomplete
    user_presets_path: str
    def __init__(self, conanfile, generator: Incomplete | None = ...) -> None: ...
    def _context(self): ...
    @property
    def content(self): ...
    def generate(self) -> None: ...
    def _get_generator(self, recipe_generator): ...
