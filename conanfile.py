from conans import ConanFile, tools
import os


class HsmConan(ConanFile):
    name = "hsm"
    description = "Finite state machine library based on the boost hana meta programming library"
    topics = ("conan", "hsm", "finite-state-machine")
    url = "https://github.com/bincrafters/conan-hsm"
    homepage = "https://github.com/erikzenker/hsm"
    license = "MIT"
    settings = "compiler"
    no_copy_source = True
    requires = "boost/1.72.0"

    @property
    def _source_subfolder(self):
        return os.path.join(self.source_folder, "source_subfolder")

    def configure(self):
        minimal_cpp_standard = "17"
        if self.settings.compiler.cppstd:
            tools.check_min_cppstd(self, minimal_cpp_standard)
        minimal_version = {
            "gcc": "6",
            "clang": "3.9",
            "apple-clang": "10",
            "Visual Studio": "17"
        }
        compiler = str(self.settings.compiler)
        if compiler not in minimal_version:
            self.output.warn(
                "%s recipe lacks information about the %s compiler standard version support." % (self.name, compiler))
            self.output.warn(
                "%s requires a compiler that supports at least C++%s." % (self.name, minimal_cpp_standard))
            return
        version = tools.Version(self.settings.compiler.version)
        if version < minimal_version[compiler]:
            raise ConanInvalidConfiguration("%s requires a compiler that supports at least C++%s." % (self.name, minimal_cpp_standard))

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def package(self):
        include_folder = os.path.join(self._source_subfolder, "include")
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        self.copy(pattern="*", dst=os.path.join("src", "include"), src=include_folder)

    def package_id(self):
        self.info.header_only()
