# Base imports
from collections import defaultdict
import os

# Relative imports
from github_tools import get_repos
from module import Module


class Registry:
    """
    A class that manages the modules in an index registry.
        - Assumes that it is located in the folder `.github/tools`
          relative to the base directory.
        - It is able to manage each module in the index registry.
    """

    def __init__(self):

        # Set the modules path.
        self._modules_path = os.getcwd() + "/modules"
        """String representing the path to the modules folder."""

        # Initialize the module dict.
        self._modules = defaultdict(lambda: None)
        """Dict of modules: {str name, Module module}."""

        # Initialize modules
        self._init_modules()

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

    def _save_version(self, module_name: str):
        module = self._modules[module_name]
        if module is not None:
            module.save_version()
        else:
            raise RuntimeError(f"Module {module_name} is None.")
