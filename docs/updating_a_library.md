# Updating a Bazel library

In this example, we assume you're making an update to `libfluent`, with the version number `2.6.4`.

Make the PR in `libfluent`.  
Make sure to bump the version in `libfluent/MODULE.bazel`.

If needed: After the PR has merged, tag the repo. Note: The tag is automatically created in most repos, but `libfluent` is an exception.

```bash
git tag 2.6.4
git push origin 2.6.4
```

## Create the package in `index-registry`

There is a GitHub action that automates creating the new library version.

Go to the [index-registry](https://github.com/Pattern-Labs/index-registry), action [call_add_module](https://github.com/Pattern-Labs/index-registry/actions/workflows/call_add_module.yml).

Click "Run workflow":

- Branch: main
- Name of module: libfluent
- Version to add: 2.6.4

This will create a new commit in the index registry repo, adding 2.6.4. It should take a minute or so.

## Update modules that depend on `libfluent`

Find modules that depend on libfluent. This assumes you have them checked out locally. (I'm not sure how to search for dependencies in GitHub.)  
This assumes all your packages are checked out in `~/code`.

```console
$ grep -w libfluent ~/code/*/MODULE.bazel
code/libfluent/MODULE.bazel:    name = "libfluent",
code/pattern_tools/MODULE.bazel:bazel_dep(name = "libfluent", version = "2.6.3")
```

For each dependency (in this case, `pattern_tools`), create a PR that updates the `libfluent` version number.
