# -*- coding: utf-8 -*-

import os
from conanfile_base import ConanFileBase


class ConanFileDefault(ConanFileBase):
    name = "vulkan_lunarg"
    exports = ConanFileBase.exports + ["conanfile_base.py"]
    settings = "os", "arch"

    _is_installer = False

    def package(self):
        if self.settings.os == "Windows":
            base_folder = os.path.join(self.build_folder, self._source_subfolder)
            if self.settings.arch == "x86":
                lib_folder = os.path.join(base_folder, "Lib32")
                bin_folder = os.path.join(base_folder, "Bin32")
                runtimebin_folder = os.path.join(base_folder, "RunTimeInstaller", "x86")
            elif self.settings.arch == "x86_64":
                lib_folder = os.path.join(base_folder, "Lib")
                bin_folder = os.path.join(base_folder, "Bin")
                runtimebin_folder = os.path.join(base_folder, "RunTimeInstaller", "x64")
            self.copy(pattern="*", dst="lib", src=lib_folder)
            self.copy(pattern="*.dll", dst="bin", src=bin_folder)
            self.copy(pattern="*.pdb", dst="bin", src=bin_folder)
            self.copy(pattern="*.json", dst="bin", src=bin_folder)
            self.copy(pattern="*", dst="include", src=os.path.join(base_folder, "Include"))
            self.copy(pattern="*", dst="bin", src=runtimebin_folder)
            self.copy(pattern="LICENSE.txt", dst="licenses", src=base_folder)
        elif self.settings.os == "Linux":
            base_folder = os.path.join(self.build_folder, self._source_subfolder)
            base_pkg_folder = os.path.join(base_folder, str(self.settings.arch))
            self.copy(pattern="*", dst="include", src=os.path.join(base_pkg_folder, "include"))
            self.copy(pattern="*", dst="lib", src=os.path.join(base_pkg_folder, "lib"))
            self.copy(pattern="*", dst="bin", src=os.path.join(base_pkg_folder, "bin"))
            self.copy(pattern="*", dst="etc", src=os.path.join(base_pkg_folder, "etc"))
            self.copy(pattern="LICENSE.txt", dst="licenses", src=base_folder)
        elif self.settings.os == "Macos":
            base_folder = os.path.join(self.build_folder, self._source_subfolder, "macOS")
            self.copy(pattern="*", dst="include", src=os.path.join(base_folder, "include"))
            self.copy(pattern="*", dst="lib", src=os.path.join(base_folder, "lib"))
            self.copy(pattern="*", dst="bin", src=os.path.join(base_folder, "bin"))
            self.copy(pattern="*", dst="etc", src=os.path.join(base_folder, "etc"))
            self.copy(pattern="*", dst="Frameworks", src=os.path.join(base_folder, "Frameworks"))

    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.libs = ["vulkan-1"]
        else:
            self.cpp_info.libs = ["vulkan"]
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.bindirs = ["bin"]
        self.cpp_info.libdirs = ["lib"]
