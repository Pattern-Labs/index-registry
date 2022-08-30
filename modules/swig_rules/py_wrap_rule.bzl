def _rules_extension(ctx):
    ctx.exports_files(
        ["swig_rules.bzl"],
    )
    ctx.filegroup(name = "swig_includes", srcs = glob(["*.i"]))
    ctx.filegroup(name = "swig_file_appender", srcs = ["swig_file_appender.py"])

rules_extension = module_extension(
    implementation = _rules_extension,
)
