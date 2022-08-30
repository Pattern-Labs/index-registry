package(default_visibility = ["//visibility:public"])

exports_files(
    [
        "swig_rules.bzl",
    ],
)

filegroup(
    name = "swig_includes",
    srcs = glob(["*.i"]),
)

filegroup(
    name = "swig_file_appender",
    srcs = ["swig_file_appender.py"],
)
