# Base imports
import os
from collections import defaultdict

# Relative imports
from bazel_version import BazelVersion
from github_tools import Version


class Module:
    """
    A class to manage a single module. Contains all information
    from a Module.bazel file and is able to edit the file.
    """

    def __init__(self, module_name: str):
        # Get the cwd.
        self._cwd = os.getcwd()
        """String representing the cwd of the registry."""

        # Set the module path.
        self._module_path = self._cwd + "/modules/" + module_name
        """String representing the path to the module folder."""

        # Set module_name.
        self._module_name = module_name
        """String representing the module name of the Module."""

        # Initialize the bazel versions dict.
        self._bazel_versions = defaultdict(lambda: None)
        """
        Default dict containing versions: 
            {str version_name: Version: version_class}.
        """

        # Initialize the latest version.
        self._latest_bazel_version = None
        """The latest BazelVersion"""

        self._init_versions()

    def _init_versions(self):
        """
        A function to read an initialize the versions of a module
        """
        # Get a list of all the versions.
        version_list = os.listdir(self._module_path)

        # Add each module to the modules dict.
        for version_name in version_list:
            # Check if its a valid version.
            version_path = self._module_path + "/" + version_name
            if os.path.isdir(version_path):
                self._bazel_versions[version_name] = BazelVersion(
                    self._module_name, version_name
                )

        # Determine the latest bazel version.
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

    def save_version(self):
        self._latest_bazel_version.save_version()
