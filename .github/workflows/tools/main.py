# Base imports
import argparse

# Local imports
from registry import Registry
from module import Module


def main(args):
    if (args["local"] is None and args["index"] is None) or (
        args["local"] is not None and args["index"] is not None
    ):
        print("ERROR: Declare one of local or index.")
        parser.print_help()
        return
    if args["local"]:
        module = Module(local=True)
        if args["bump_patch"]:
            print("Bumping a local patch")
            module.bump_patch()
        if args["bump_minor"]:
            print("Bumping a local minor")
            module.bump_patch()
        if args["save_local"]:
            print("Saving a local module")
            module.save_version(override=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage the index registry.")
    parser.add_argument(
        "--local",
        action="store_true",
        required=False,
        help="In a local repo. <module_name>",
    )
    parser.add_argument(
        "--index",
        required=False,
        help="In the index registry.",
    )
    parser.add_argument(
        "--bump-patch",
        required=False,
        action="store_true",
        help="Bump a patch.",
    )
    parser.add_argument(
        "--bump-minor",
        required=False,
        action="store_true",
        help="Bump a minor..",
    )
    parser.add_argument(
        "--save-local",
        required=False,
        action="store_true",
        help="Save a single local module.",
    )
    parser.add_argument(
        "--save-version-and-dependents",
        required=False,
        help="Save version and its dependents.",
    )
    parser.add_argument(
        "--add-or-update-dependency",
        required=False,
        help="Add or update a dependency.",
    )

    args = vars(parser.parse_args())
    main(args)
