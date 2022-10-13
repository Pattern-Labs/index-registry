# Adding a Library
This tutorial assumes you've cloned this repository, and are starting out with your pwd at its root. This tutorial best applies for dependencies with their code on github, and for which a bazel BUILD file already exists, or can be crafted. 

For demonstration, this tutorial will walkthrough adding the "FreeRTOS" module.

Run `tools/add_module.py` script. This will prompt you with a series of questions.
1. Module name? `FreeRTOS`
2. Module version? `202112.00` (The most recent release from FreeRTOS' github page.)
3. Compatibility level? Default is fine.
4. URL of the source archive? `https://github.com/FreeRTOS/FreeRTOS/releases/download/202112.00/FreeRTOSv202112.00.zip` (Download link of the source code from that most-recent release.)
5. Archive's strip_prefix value? `FreeRTOSv202112.00` (Usually the name of the archive file without extension.)
6. Do you want to add patch files? `N` (Patch files can be used, if needed, to make arbitrary modifications to the downloaded files.)
7. Do you want to add a BUILD file? `y`
8. Please enter the path of the BUILD file to be added: `FreeRTOS.BUILD` (This is implemented as another patch file, which just copies the BUILD file into the downloaded code's root directory. See [below](#the-build-file) for the file used in this example.)
9. Do you want to specify a MODULE.bazel file? `N` (This would be used to get the (bzlmod) dependencies of the new library.)
10. Do you want to specify dependencies for thsi module? `y`
11. Enter dependencies: `rules_cc@0.0.2` (Not sure if this is actually needed for FreeRTOS.)
12. Do you want to specify an existing presubmit.yml file? `N`
13. List build targets: `//` (This is used to generate a presubmit.yml file, but we aren't yet using that functionality so this can be anything for now.)
14. Do you have a test module in your source archive? `n`
14. Please enter the homepage url for this module: `https://github.com/FreeRTOS/FreeRTOS`
15. Do you want to add a maintainer for this module? `N`

After all that, the python script will generate a `.json` file in your current directory with everything you input. The filename includes the module name and a timestamp. Mine was `FreeRTOS.20221013-120221.json`, and looked like this:
```
{
    "build_file": "FreeRTOS.BUILD",
    "compatibility_level": "1",
    "deps": [
        [
            "rules_cc",
            "0.0.2"
        ]
    ],
    "module_dot_bazel": null,
    "name": "FreeRTOS",
    "patch_strip": 0,
    "patches": [],
    "strip_prefix": "FreeRTOSv202112.00",
    "url": "https://github.com/FreeRTOS/FreeRTOS/releases/download/202112.00/FreeRTOSv202112.00.zip",
    "version": "202112.00"
}
```
The script will then attempt to create the module based on this information. If anything goes wrong/needs tweaking, just update the `.json` (and/or `.BUILD` file) and re-run the script like this:
```
> tools/add_module.py --input FreeRTOS.20221013-120221.json
```

Once things are working well, remove the `presubmit.yml` file that got generated and submit a PR with the rest that adds the new dependency to the registry!

### The BUILD File

The `FreeRTOS.BUILD` file referenced above looks like this:

```
package(default_visibility = ["//visibility:public"])

cc_library(
    name = "freertos_lib",
    srcs = glob([
        "FreeRTOS/Source/*.c",
        "FreeRTOS/Source/portable/*.c",
        "FreeRTOS/portable/*.S",
    ]),
    hdrs = glob([
        "FreeRTOS/Source/include/*.h",
    ]),
    strip_include_prefix = "FreeRTOS/Source/include/",
    deps = [
        "freertos_portable",
        "@//:freertos_config",
    ],
    alwayslink = True,
)

cc_library(
    name = "freertos_portable",
    hdrs = glob([
        "FreeRTOS/Source/portable/*.h",
    ]),
    strip_include_prefix = "FreeRTOS/Source/portable/",
)

cc_library(
    name = "freertos_plus_tcp_lib",
    srcs = glob([
        "FreeRTOS-Plus/Source/FreeRTOS-Plus-TCP/*.c",
        "FreeRTOS-Plus/Source/FreeRTOS-Plus-TCP/portable/**.c",
        "FreeRTOS-Plus/Source/FreeRTOS-Plus-TCP/portable/**.s",
    ]),
    hdrs = glob([
        "FreeRTOS-Plus/Source/FreeRTOS-Plus-TCP/include/**.h",
    ]),
    strip_include_prefix = "FreeRTOS-Plus/Source/FreeRTOS-Plus-TCP/include/",
    deps = [
        "@freertos//:freertos_lib",
        "freertos_plus_tcp_portable",
        "@//:freertos_config",
    ],
    alwayslink = True,
)

cc_library(
    name = "freertos_plus_tcp_portable",
    hdrs = glob([
        "FreeRTOS-Plus/Source/FreeRTOS-Plus-TCP/portable/**.h",
    ]),
    strip_include_prefix = "FreeRTOS-Plus/Source/FreeRTOS-Plus-TCP/portable/",
)
```
but there are several other examples available in the index registry already. Check out `msgpack` for an example that uses bazel's `rules_foreign_cc` to just use the existing cmake build structure.
