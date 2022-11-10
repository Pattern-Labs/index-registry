# Base imports
import argparse

# Local imports
# TODO (Thomas Gira) Automation
# from registry import Registry
from module import Module


def main(args):
    if (args["local"] is False and args["index"] is False) or (
        args["local"] is True and args["index"] is True
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
        if args["update_dependency"] is not None:
            dependency = args["update_dependency"][0]
            version = args["update_dependency"][1]
            print(f"Updating the dependency {dependency} to version {version}")
            module.add_or_update_dependency(dependency=dependency, version=version)

        # These need to be last. Order matters.
        if args["export_tag"]:
            module.export_version_to_github_env()
        if args["save_local"]:
            print("Saving a local module")
            module.save_version(override=True)
    elif args["index"]:
        # TODO (Thomas Gira) Automation
        # index = Registry()
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage the index registry.")
    parser.add_argument(
        "--local",
        action="store_true",
        required=False,
        help="In a local repo.",
    )
    parser.add_argument(
        "--index",
        action="store_true",
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
        "--export-tag",
        required=False,
        action="store_true",
        help="Export the current tag as a github enivornment variable..",
    )
    parser.add_argument(
        "--update-dependency",
        required=False,
        nargs=2,
        help="update a dependency",
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
        help="Add or update a dependency. --add-or-update-dependency <dependency> <version>",
    )

    args = vars(parser.parse_args())
    main(args)
