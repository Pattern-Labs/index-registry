def _logging_lib(ctx):
    ctx.cc_library(
        name = "pattern_cpp_logging",
        hdrs = ["logging.h"],
        include_prefix = "pattern_cpp_logging",
        deps = [
            "@com_github_google_glog//:glog",
        ],
        alwayslink = True,
    )

logging_lib = module_extension(
    implementation = _logging_lib,
)
