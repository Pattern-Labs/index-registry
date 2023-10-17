# Index Registry Workflows

Currently the index registry contains a sample of tools and workflows in order to maintain versioning and dependencies in bazel mod. There are three main workflows each with distinct purposes: Add Module, Bump version and Update Dependency.

## Workflows

Here is a high level overview of workflows and how/when to use them. Each workflow is implemented as a `workflow_call`, each with a complimentary `workflow_dispatch` that allows for manual triggering. The order of them in this document is the order in which you should call the functions to update any given module.

1. **Bump Version (`bumpy_version.yml`):** This workflow allows you to bump the semver version of a module. It can bump either a patch or a minor. It will also update the MODULE.bazel file in the repo so you then can call `Add Module`.
1. **Add Module (`add_module.yml`):** This workflow will add a module at a specified version to the index registry. It needs to be called after the specified module has been tagged at the version corresponding to the workflow call and to what is in its MODULE.bazel file in the repo.
1. **Update Dependency (`update_dependency.yml`):** This workflow allows you to update the dependency of a module. You specify the dependent module the dependency module and the version of the dependency. It will check out the dependent repo and update its MODULE.bazel file. Thereafter you will need to repeat the same process for the dependent module that the dependency was added to.
