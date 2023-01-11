# Base imports
from collections import defaultdict
from typing import List
import os

# Relative imports
from bazel_version import BazelVersion
from github_tools import Version


class Module:
    """
    A class to manage a single module. Contains all information
    from a Module.bazel file and is able to edit the file.
    """

    def __init__(
        self, module_name: str = None, local: bool = False, module_path="local_repo"
    ):
        self._local = local
        if local:
            self._cwd = os.getcwd()
            """String representing the cwd of the repo."""

            self._module_path = self._cwd + "/" + module_path
            """String representing the path to the module folder."""
        else:
            self._cwd = os.getcwd()
            """String representing the cwd of the registry."""

            self._module_path = self._cwd + "/modules/" + module_name
            """String representing the path to the module folder."""

        self._module_name = module_name
        """String representing the module name of the Module."""

        self._bazel_versions = defaultdict(lambda: None)
        """
        Default dict containing versions: 
            {str version_name: Version: version_class}.
        """

        self._latest_bazel_version = None
        """The latest BazelVersion"""

        self._init_versions()

    def _init_versions(self):
        """A function to read and initialize the versions of a module."""
        if self._local:
            self._latest_bazel_version = BazelVersion(self._module_name, local=True)
        else:
            version_list = os.listdir(self._module_path)

            for version_name in version_list:
                version_path = self._module_path + "/" + version_name
                if os.path.isdir(version_path):
                    self._bazel_versions[version_name] = BazelVersion(
                        self._module_name, version_name
                    )

            bazel_versions = list(self._bazel_versions.values())
            latest_version = Version()
            for bazel_version in bazel_versions:
                if bazel_version.get_version() > latest_version:
                    latest_version = bazel_version.get_version()
                    self._latest_bazel_version = bazel_version

    def bump_patch(self):
        self._latest_bazel_version.bump_patch()

    def bump_minor(self):
        self._latest_bazel_version.bump_minor()

    def bump_major(self):
        self._latest_bazel_version.bump_major()

    def save_version(self, override=False):
        self._latest_bazel_version.save_version(override=override)

    def add_or_update_dependency(self, dependency, version):
        self._latest_bazel_version.add_or_update_dependency(dependency, version)

    @property
    def latest_bazel_version(self) -> BazelVersion:
        return self._latest_bazel_version

    @property
    def dependencies(self) -> List[str]:
        return self._latest_bazel_version.dependencies

    @property
    def name(self) -> str:
        return self._module_name

    def export_version_to_github_env(self):
        self._latest_bazel_version.export_version_to_github_env()
