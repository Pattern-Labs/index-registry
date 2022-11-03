# Import necessary libraries
# Base imports
from collections import defaultdict
import argparse
import os

# Relative imports
from github_tools import get_repos
from module import Module
from leaf import Leaf


class Registry:
    """
    A class that manages the modules in an index registry.
        - Assumes that it is located in the folder `.github/tools`
          relative to the base directory.
        - It is able to manage each module in the index registry.
    """

    def __init__(self):
        # Get the cwd.
        self._cwd = os.getcwd()
        """String representing the cwd of the registry."""

        # Set the modules path.
        self._modules_path = self._cwd + "/modules"
        """String representing the path to the modules folder."""

        # Initialize the module dict.
        self._modules = defaultdict(lambda: None)
        """Dict of modules: {str name, Module module}."""

        # Initialize the root of the tree.
        self._dependency_tree = []

        # Initialize modules
        self._init_modules()

        # Resolve dependencies
        self._resolve_dependencies()

        # Display the dependency graph.
        for leaf in self._dependency_tree:
            leaf.print()

        # Initialize the depth dict.
        self._depth = defaultdict(lambda: -1)
        """Dict representing the depth of each module"""

        # Resolve the depth map.
        self._resolve_depths()

    def _add_depth(self, leaf: Leaf, depth: int = 0):
        if depth > self._depth[leaf.name]:
            self._depth[leaf.name] = depth
        for child in leaf.children:
            self._add_depth(child, depth + 1)

    def _resolve_depths(self):
        for leaf in self._dependency_tree:
            self._add_depth(leaf)
        self._depth = defaultdict(
            lambda: -1,
            sorted(self._depth.items(), key=lambda item: item[1], reverse=True),
        )

    def _resolve_dependencies(self):
        for module in self._modules.values():

            def add_dependency(
                leaf: Leaf,
                dependency: str,
                root: Leaf,
                remove_from_dependency_tree: bool = False,
            ) -> Leaf:
                if leaf.name == dependency:
                    root.add_child(leaf)
                    for root_leaf in self._dependency_tree:
                        if root_leaf.name == leaf.name:
                            remove_from_dependency_tree = True
                for child in leaf.children:
                    (new_child, remove_from_dependency_tree) = add_dependency(
                        child, dependency, root, remove_from_dependency_tree
                    )
                return (root, remove_from_dependency_tree)

            def add_to_dependents(leaf: Leaf, new_leaf: Leaf) -> bool:
                root = True
                # Check children
                for index, child in enumerate(leaf.children):
                    (leaf_result, root_result) = add_to_dependents(child, new_leaf)
                    leaf.replace_child(index, leaf_result)
                    root = root and root_result
                # Check self.
                for dependency in leaf.dependencies:
                    if dependency == new_leaf.name:
                        leaf.add_child(new_leaf)
                        return (leaf, root)
                return (leaf, root)

            # Initialize the new leaf.
            new_leaf = Leaf(module)
            root = True

            # Add the leafs dependencies.
            remove_indices = []
            for dependency in module.dependencies:
                for index, leaf in enumerate(self._dependency_tree):
                    (new_leaf, remove_from_dependency_tree) = add_dependency(
                        leaf, dependency, new_leaf
                    )
                    if remove_from_dependency_tree:
                        remove_indices += [index]

            # Remove any root dependencies.
            for index in sorted(remove_indices, reverse=True):
                self._dependency_tree.pop(index)

            # Add leaf to dependents:
            for leaf in self._dependency_tree:
                (leaf, root) = add_to_dependents(leaf, new_leaf)

            # Add to root if root.
            if root:
                self._dependency_tree.append(new_leaf)

    def _init_modules(self):
        """
        A function to read in and initialize the modules in the registry.
        """
        # Get a list of all the modules.
        module_list = os.listdir(self._modules_path)

        # Get a list of pattern repos.
        repo_list = get_repos() + ["pattern_tools"]
        # Add each module to the modules dict.
        for module_name in module_list:
            # Check if the it is a valid module.
            module_path = self._modules_path + "/" + module_name
            if os.path.isdir(module_path) and module_name in repo_list:
                self._modules[module_name] = Module(module_name)

    def _resolve_update(self, module_name: str):
        self._resolve_dependencies()
        self._resolve_depths()

        depth = self._depth[module_name]

        updates_list = []
        for key, value in self._depth.items():
            if value < depth:
                updates_list += [key]
        self._add_github_env_variable("PATTERN_UPDATES_LIST", updates_list)

    def _bump_patch(self, module_name: str):
        module = self._modules[module_name]
        if module is not None:
            module.bump_patch()
        else:
            raise RuntimeError(f"Module {module_name} is None.")

    def bump_patch(self, module_name: str):
        self._bump_patch(module_name=module_name)
        self._resolve_update(module_name=module_name)

    def _bump_minor(self, module_name: str):
        module = self._modules[module_name]
        if module is not None:
            module.bump_minor()
        else:
            raise RuntimeError(f"Module {module_name} is None.")

    def bump_minor(self, module_name: str):
        self._bump_minor(module_name=module_name)
        self._resolve_update(module_name=module_name)

    def _bump_major(self, module_name: str):
        module = self._modules[module_name]
        if module is not None:
            module.bump_major()
        else:
            raise RuntimeError(f"Module {module_name} is None.")

    def bump_major(self, module_name: str):
        self._bump_major(module_name=module_name)
        self._resolve_update(module_name=module_name)

    def _save_version(self, module_name: str):
        module = self._modules[module_name]
        if module is not None:
            module.save_version()
        else:
            raise RuntimeError(f"Module {module_name} is None.")

    def save_version(self, module_name):
        self._save_version(module_name)

    def save_version_and_dependents(self, module_name):
        self._resolve_dependencies()
        self._resolve_depths()

        depth = self._depth[module_name]
        self._save_version(module_name)
        for key, value in self._depth.items():
            if value < depth:
                self._save_version(key)

    def add_or_update_dependency(self, dependency, version, dependent):
        self._add_or_update_dependency(self, dependency, version, dependent)
        self._resolve_dependencies()
        self._resolve_depths()

    def add_or_update_dependents(self, dependency, version):
        depth = self._depth[dependency]
        for key, value in self._depth.items():
            if value < depth:
                self._add_or_update_dependency(self, dependency, version, key)
        self._resolve_dependencies()
        self._resolve_depths()

    def _add_or_update_dependency(self, dependency, version, dependent):
        self._modules[dependent].add_or_update_dependency(dependency, version)

    def _add_github_env_variable(self, key: str, value: str):
        env_variable_location = os.environ.get("GITHUB_ENV")
        if env_variable_location is None:
            raise RuntimeError(
                "Attempted to add a github env variable while not in a runner."
            )
        with open(env_variable_location, "a") as file:
            file.write(f"{key}={value}\n")
