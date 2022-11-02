from typing import List
import requests
import os
import re


class Version:
    def __init__(self, major: int = 0, minor: int = 0, patch: int = 0):
        self._major = int(major)
        self._minor = int(minor)
        self._patch = int(patch)

    @property
    def major(self) -> int:
        return self._major

    @property
    def minor(self) -> int:
        return self._minor

    @property
    def patch(self) -> int:
        return self._patch

    def bump_major(self):
        self._major += 1
        self._minor = 0
        self._patch = 0

    def bump_minor(self):
        self._minor += 1
        self._patch = 0

    def bump_patch(self):
        self._patch += 1

    def get_tag(self) -> str:
        return f"{self._major}.{self._minor}.{self._patch}"

    def export_to_env_variable(self, env_variable: str = "PATTERN_VERSION_TAG"):
        os.environ[env_variable] = self.get_tag()
        print(f"set {env_variable} to {os.environ[env_variable]}")

    def __gt__(self, other: "Version") -> bool:
        if not isinstance(other, Version):
            raise TypeError("Comparison is not of Version type")

        major_greater_than = self.major > other.major
        minor_greater_than = self.minor > other.minor
        patch_greater_than = self.patch > other.patch

        major_equal_to = self.major == other.major
        minor_equal_to = self.minor == other.minor

        if major_greater_than:
            return True

        if major_equal_to and minor_greater_than:
            return True

        if major_equal_to and minor_equal_to and patch_greater_than:
            return True

        return False


def get_tags(repo: str, owner: str = "pattern-labs", token: str = None) -> dict:
    """Function to get a list of tags in a given repo"""
    if token is None:
        token = os.environ.get("PATTERN_GITHUB_TOKEN")
    if token is not None:
        url = f"https://api.github.com/repos/{owner}/{repo}/tags"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        r = requests.get(url, headers=headers)
        return r.json()
    raise RuntimeError("No github token found")


def get_releases(repo: str, owner: str = "pattern-labs", token: str = None) -> dict:
    """Function to get a list of releases in a given repo"""
    if token is None:
        token = os.environ.get("PATTERN_GITHUB_TOKEN")
    if token is not None:
        url = f"https://api.github.com/repos/{owner}/{repo}/releases"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        r = requests.get(url, headers=headers)
        return r.json()
    raise RuntimeError("No github token found")


def list_releases(
    repo: str, owner: str = "pattern-labs", token: str = None
) -> List[Version]:
    """Function to get an integer list of weekly releases"""
    releaseRegex = re.compile(r"^([0-9]*)\.([0-9]*)\.([0-9]*)")
    query = get_releases(repo=repo, owner=owner, token=token)
    versions = []
    for item in query:
        version = item["name"]
        match = releaseRegex.search(version)
        if match is not None and match == version:
            major = int(match.group(1))
            minor = int(match.group(2))
            patch = int(match.group(3))
            version = Version(major=major, minor=minor, patch=patch)
            versions.append(version)
    return versions


def list_tags(
    repo: str, owner: str = "pattern-labs", token: str = None
) -> List[Version]:
    """Function to get an integer list of weekly releases"""
    releaseRegex = re.compile(r"^([0-9]*)\.([0-9]*)\.([0-9]*)")
    query = get_tags(repo=repo, owner=owner, token=token)
    versions = []
    for item in query:
        version = item["name"]
        match = releaseRegex.search(version)
        if match is not None and match.group() == version:
            major = int(match.group(1))
            minor = int(match.group(2))
            patch = int(match.group(3))
            version = Version(major=major, minor=minor, patch=patch)
            versions.append(version)
    return versions


def last_weekly_release(
    repo: str, owner: str = "pattern-labs", token: str = None
) -> Version:
    """Function to get the value of the most recent weekly release."""
    versions = list_releases(repo=repo, owner=owner, token=token)
    largest_version = Version()
    for version in versions:
        if version > largest_version:
            largest_version = version
    return largest_version


def last_tag(repo: str, owner: str = "pattern-labs", token: str = None) -> Version:
    """Function to get the value of the most recent weekly release."""
    versions = list_tags(repo=repo, owner=owner, token=token)
    largest_version = get_largest_version(versions)
    return largest_version


def get_largest_version(versions: List[Version]) -> Version:
    largest_version = Version()
    for version in versions:
        if version > largest_version:
            largest_version = version
    return largest_version


def bump_major(repo: str, owner: str = "pattern-labs", token: str = None) -> str:
    version = last_tag(repo=repo, owner=owner, token=token)
    version.bump_major()
    return version.get_tag()


def bump_minor(repo: str, owner: str = "pattern-labs", token: str = None) -> str:
    version = last_tag(repo=repo, owner=owner, token=token)
    version.bump_minor()
    return version.get_tag()


def bump_patch(repo: str, owner: str = "pattern-labs", token: str = None) -> str:
    version = last_tag(repo=repo, owner=owner, token=token)
    version.bump_patch()
    return version.get_tag()


def get_repos(owner: str = "pattern-labs", token: str = None) -> List[str]:
    """Function to get a list of repos from a given owner"""
    if token is None:
        token = os.environ.get("PATTERN_GITHUB_TOKEN")
    if token is not None:
        url = f"https://api.github.com/orgs/{owner}/repos"
        headers = {
            "Authorization": f"Bearer {token}",
        }
        params = {"per_page": 100, "sort": "pushed"}
        repos = requests.get(url, headers=headers, params=params).json()
        repo_list = []
        for repo in repos:
            repo_list.append(repo["name"])

        return repo_list
    raise RuntimeError("No github token found")
