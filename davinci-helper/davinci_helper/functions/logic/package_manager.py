"""
Distro-aware wrapper around the system package manager.

Usage:
        from davinci_helper.package_manager import package_manager
        libs = package_manager.list_installed_libs()
        package_manager.install(["libcurl", "mesa-libGLU"])
"""

import subprocess, sys, re
from abc import ABC, abstractmethod


class PackageManager(ABC):
    """Package manager interface for listing and installing libraries."""
    @abstractmethod
    def list_installed_libs(self) -> subprocess.CompletedProcess: ...
    @abstractmethod
    def install(self, pkgs: list[str]) -> subprocess.CompletedProcess: ...


class DnfManager(PackageManager):
    """Package manager for Fedora and RHEL-based distributions using DNF."""
    def list_installed_libs(self):
        return subprocess.run(["dnf", "list", "--installed"],
                              capture_output=True, text=True)

    def install(self, pkgs: list[str]):
        return subprocess.run(
            ["dnf", "install", "-y", *pkgs],
            shell=True,
            capture_output=True,
            text=True
        )

class AptManager(PackageManager):
    """Package manager for Debian and Ubuntu-based distributions using APT."""
    def list_installed_libs(self):
        return subprocess.run(["dpkg", "-l"],
                              capture_output=True, text=True)

    def install(self, pkgs: list[str]):
        subprocess.check_call(["apt", "update", "-qq"])
        return subprocess.run(
            ["apt", "install", "-y", *pkgs],
            shell=True,
            capture_output=True,
            text=True
        )

def _detect_backend() -> PackageManager:
    """Detect the package manager backend based on the distribution type."""
    try:
        with open("/etc/os-release") as f:
            # find all key=value pairs in os-release file
            data = dict(re.findall(r"^(\w+)=(.*)", f.read(), re.M))
            # ID_LIKE identifies the distribution family (debian, fedora, etc.)
            id_like = data.get("ID_LIKE", "").lower()
    except FileNotFoundError:
        id_like = ""

    if "debian" in id_like:
        return AptManager()
    if "fedora" in id_like:
        return DnfManager()

    print(
        "davinci-helper: unsupported distribution "
        "(ID_LIKE neither 'debian' nor 'fedora').", file=sys.stderr)
    sys.exit(1)

# package manager singleton instance
package_manager: PackageManager = _detect_backend()
