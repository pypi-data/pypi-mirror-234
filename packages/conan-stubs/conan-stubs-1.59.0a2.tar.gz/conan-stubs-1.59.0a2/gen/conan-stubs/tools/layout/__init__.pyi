from conan.tools.cmake import cmake_layout as cmake_layout
from conan.tools.google import bazel_layout as bazel_layout
from conan.tools.microsoft import vs_layout as vs_layout

def basic_layout(conanfile, src_folder: str = ...) -> None: ...
