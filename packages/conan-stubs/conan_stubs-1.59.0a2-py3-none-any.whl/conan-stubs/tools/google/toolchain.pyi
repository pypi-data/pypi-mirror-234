from _typeshed import Incomplete
from conan.tools._check_build_profile import check_using_build_profile as check_using_build_profile
from conan.tools.files.files import save_toolchain_args as save_toolchain_args

class BazelToolchain:
    _conanfile: Incomplete
    _namespace: Incomplete
    def __init__(self, conanfile, namespace: Incomplete | None = ...) -> None: ...
    def generate(self) -> None: ...
