# Base imports
import argparse

# Local imports
# TODO (Thomas Gira) Automation
# from registry import Registry
from module import Module


def main(args):
    if args["local"]:
        module = None
        if args["bump_patch"]:
            module = Module(local=True, module_name=args["module_name"][0])
            print("Bumping a local patch")
            module.bump_patch()
        if args["bump_minor"]:
            module = Module(local=True, module_name=args["module_name"][0])
            print("Bumping a local minor")
            module.bump_minor()
        if args["bump_major"]:
            module = Module(local=True, module_name=args["module_name"][0])
            print("Bumping a local major")
            module.bump_major()
        if args["update_dependency"] is not None:
            module = Module(local=True, module_name=args["module_name"][0])
            dependency = args["update_dependency"][0]
            version = args["update_dependency"][1]
            print(f"Updating the dependency {dependency} to version {version}")
            module.add_or_update_dependency(dependency=dependency, version=version)
        if args["check_version_bump"]:
            main_module = Module(
                local=True, module_name=args["module_name"][0], module_folder="main"
            )
            incoming_module = Module(
                local=True,
                module_name=args["module_name"][0],
                module_folder="incoming",
            )
            main_version = main_module.latest_bazel_version.version
            incoming_version = incoming_module.latest_bazel_version.version

            if not incoming_version > main_version:
                raise RuntimeError(
                    f"Incoming version of {incoming_version} is not greater than main@{main_version}"
                )

        # These need to be last. Order matters.
        if args["export_tag"]:
            if module == None:
                module = Module(local=True, module_name=args["module_name"][0])
            module.export_version_to_github_env()
        if args["save_local"]:
            if module == None:
                module = Module(local=True, module_name=args["module_name"][0])
            print("Saving a local module")
            module.save_version(override=True)
    elif args["index"]:
        # TODO (Thomas Gira) Automation
        # index = Registry()
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage the index registry.")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument(
        "--local",
        action="store_true",
        help="In a local repo.",
    )
    action.add_argument(
        "--index",
        action="store_true",
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
        help="update a dependency --update-dependency <dependency> <version>",
    )
    parser.add_argument(
        "--save-local",
        required=False,
        action="store_true",
        help="Save a single local module.",
    )
    parser.add_argument(
        "--module-name",
        required=False,
        nargs=1,
        help="Set local module name",
    )
    parser.add_argument(
        "--check-version-bump",
        required=False,
        action="store_true",
        help="Check if the incoming version is greater than the one at main. Raise exit 0 if so.",
    )
    args = vars(parser.parse_args())
    main(args)
