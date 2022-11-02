from github_tools import bump_minor
import argparse


parser = argparse.ArgumentParser(description="Manage versions.")
parser.add_argument(
    "--repo",
    required=True,
    help="The repo you want.",
)
parser.add_argument(
    "--owner",
    default="pattern-labs",
    required=False,
    help="The owner you want.",
)
parser.add_argument(
    "--token",
    required=False,
    help="Repo access token.",
)

args = vars(parser.parse_args())
repo = args["repo"]
owner = args["owner"]
token = args["token"]

bump_minor(repo=repo, owner=owner, token=token)
