# Base imports
from collections import defaultdict
import os
import re
import json
import base64
import hashlib
import requests

# Local imports
from github_tools import Version


class BazelVersion:
    """
    A class containing the version information of a bazel module.
    """

    VERSION_REGEX = re.compile(r"([0-9]+).([0-9]+).([0-9]+)")
    MODULE_START_REGEX = re.compile(r"module\(")
    MODULE_END_REGEX = re.compile(r"[)]")
    MODULE_NAME_REGEX = re.compile(r'( +name = ")(\w*)(",)')
    MODULE_VERSION_REGEX = re.compile(r'( +version = ")(.*)(",)')
    MODULE_COMPATIBILITY_REGEX = re.compile(r"( +compatibility_level = )([0-9]*)(,)")
    BAZEL_DEP_REGEX = re.compile(
        r'bazel_dep\(name = "(\w*)", version = "([0-9]*.[0-9]*.[0-9]*)'
    )
    COMMAND_REGEX = re.compile(r'(\w+) = (\w+)[(]"([^"]+)", "([^"]+)"[)]')

    def __init__(self, module_name: str, version_name: str):
        # Get the cwd.
        self._cwd = os.getcwd()
        """String representing the cwd of the registry."""

        # Set the version path.
        self._version_path = self._cwd + "/modules/" + module_name + "/" + version_name
        """String representing the path to the version folder."""

        # Set module name.
        self._module_name = module_name
        """String representing the name of the module the version is contained in."""

        # Set Version object.
        version_match = self.VERSION_REGEX.search(version_name)
        if version_match is None:
            raise RuntimeError(f"Invalid version for {module_name}@{version_name}")
        major = version_match.group(1)
        minor = version_match.group(2)
        patch = version_match.group(3)
        self._version = Version(major=major, minor=minor, patch=patch)
        """Version object representing the version of the module."""

        # Initialize the compatibility level.
        self._compatibility_level = None
        """Int representing the compatibility level."""

        # Initialize the bazel_deps
        self._bazel_deps = []
        """List of bazel dependencies."""

        # Initialize other lines.
        self._other_lines = []
        """List of lines that come after bazel_deps"""

        # Initialize source
        self._source = None
        """Dict representing the source.json file"""

        # Read in the MODULE.bazel file.
        if self._parse_bazel_file() is not True:
            raise RuntimeError(
                f"Invalid bazel file for {self._module_name}@{self._version.get_tag()}"
            )

        # Read in the source.json file.
        with open(
            self._version_path + "/source.json",
        ) as f:
            self._source = json.load(f)

    def _parse_bazel_file(self):
        # Read in the MODULE.bazel file.
        with open(self._version_path + "/MODULE.bazel") as file:
            lines = file.readlines()
        # Setup conditionals.
        module_start = False
        module_end = False
        # Parse through lines.
        for line in lines:
            # Looking for start of module definition.
            if module_start is False and module_end is False:
                # Look for end of module definition.
                module_start_match = self.MODULE_START_REGEX.search(line)
                if module_start_match is not None:
                    module_start = True
                    continue

                # Look for end of module definition.
                module_end_match = self.MODULE_END_REGEX.search(line)
                if module_end_match is not None:
                    print("Module end found before module start")
                    return False

            # Adding contents of module definition.
            if module_start is True and module_end is False:
                # Look for end of module definition.
                module_end_match = self.MODULE_END_REGEX.search(line)
                if module_end_match is not None:
                    module_end = True
                    continue
                # Look for module name definition.
                module_name_match = self.MODULE_NAME_REGEX.search(line)
                if module_name_match is not None:
                    if module_name_match.group(2) != self._module_name:
                        print(
                            f"BAZEL.module name: {module_name_match.group(2)} != module_name: {self._module_name}"
                        )
                        return False
                    continue
                # Look for module version definition.
                module_version_match = self.MODULE_VERSION_REGEX.search(line)
                if module_version_match is not None:
                    if module_version_match.group(2) != self._version.get_tag():
                        print(
                            f"BAZEL.module version: {module_version_match.group(2)} != version_name: {self._version.get_tag()}"
                        )
                        return False
                    continue
                # Look for module compatibility definition.
                module_compatibility_match = self.MODULE_COMPATIBILITY_REGEX.search(
                    line
                )
                if module_compatibility_match is not None:
                    self._compatibility_level = module_compatibility_match.group(2)
                    continue

            # Add other data fields.
            if module_start is True and module_end is True:
                # Look for bazel deps.
                bazel_dep_match = self.BAZEL_DEP_REGEX.search(line)
                if bazel_dep_match is not None:
                    bazel_dep = defaultdict(lambda: None)
                    bazel_dep["name"] = bazel_dep_match.group(1)
                    bazel_dep["version"] = bazel_dep_match.group(2)
                    self._bazel_deps.append(bazel_dep)
                    continue
                else:
                    self._other_lines.append(line)

        return True

    def save_version(self, override=False):
        """
        Save the current verson.
            :param: override Override and existing matching version if present.
                    Defaults to False.
        """
        # Check for existing version.
        existing_version = os.path.isdir(self._version_path)
        if existing_version is True and override is False:
            raise RuntimeError(
                "Version that is being saved exists and override is set to false."
            )

        # Create folder.
        os.mkdir(self._version_path)

        # Write MODULE.bazel
        with open(self._version_path + "/MODULE.bazel", "w") as file:
            file.write("module(\n")
            file.write('    name = "' + self._module_name + '",\n')
            file.write('    version = "' + self._version.get_tag() + '",\n')
            file.write(
                "    compatibility_level = " + str(self._compatibility_level) + ",\n"
            )
            file.write(")\n")
            for bazel_dep in self._bazel_deps:
                file.write(
                    'bazel_dep(name = "'
                    + bazel_dep["name"]
                    + '", version = "'
                    + bazel_dep["version"]
                    + '")\n'
                )
            for line in self._other_lines:
                file.write(line)

        # Write source.json
        with open(self._version_path + "/source.json", "w", encoding="utf-8") as file:
            json.dump(self._source, file, ensure_ascii=False, indent=4)

    def get_version(self) -> Version:
        return self._version

    def _update_path(self):
        self._version_path = (
            self._cwd + "/modules/" + self._module_name + "/" + self._version.get_tag()
        )

    def _get_integrity(self) -> str:
        url = (
            '"'
            + "https://github.com/Pattern-Labs/"
            + self._module_name
            + "/archive/refs/tags/"
            + self._version.get_tag()
            + ".tar.gz"
            + "+"
        )
        try:
            data = requests.get(url).content
        except requests.exceptions.InvalidSchema:
            raise RuntimeError(
                f"Error: Tag {self._version.get_tag()} does not exist for {self._module_name}"
            )
        hash_value = hashlib.sha256(data)
        return "sha256-" + base64.b64encode(hash_value.digest()).decode()

    def _update_source(self):
        prefix = '"' + self._module_name + "-" + self._version.get_tag()
        url = (
            '"'
            + "https://github.com/Pattern-Labs/"
            + self._module_name
            + "/archive/refs/tags/"
            + self._version.get_tag()
            + ".tar.gz"
            + "+"
        )
        integrity = self._get_integrity()
        self._source["prefix"] = prefix
        self._source["url"] = url
        self._source["integrity"] = integrity

    def bump_patch(self):
        self._version.bump_patch()
        self._update_path()
        self._update_source()

    def bump_minor(self):
        self._version.bump_minor()
        self._update_path()
        self._update_source()

    def bump_major(self):
        self._version.bump_major()
        self._update_path()
        self._update_source()