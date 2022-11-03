from module import Module


class Leaf:
    def __init__(self, module: Module):
        self._module = module
        latest_bazel_version = module.latest_bazel_version
        self._dependencies = latest_bazel_version.dependencies
        self._children = []

    def add_child(self, leaf: "Leaf"):
        self._children.append(leaf)

    @property
    def name(self):
        return self._module._module_name

    @property
    def dependencies(self):
        return self._dependencies

    @property
    def children(self):
        return self._children

    def print(self, offset=0):
        spaces = " " * offset * 5
        print(f"{spaces}Leaf: {self.name} with children:")
        for child in self._children:
            child.print(offset + 1)

    def replace_child(self, index: int, child: "Leaf"):
        self._children[index] = child
