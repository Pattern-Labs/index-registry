# Copyright (C) 2022 Pattern Labs, Inc - All Rights Reserved
#   Unauthorized copying of this file, via any medium is strictly prohibited
#   Proprietary and confidential

def _include_dirs(deps):
    return depset(transitive = [dep[CcInfo].compilation_context.includes for dep in deps]).to_list()

def _headers(deps):
    return depset(transitive = [dep[CcInfo].compilation_context.headers for dep in deps]).to_list()

# Bazel rules for building swig files.
def _py_swig_gen_impl(ctx):
    module_name = ctx.attr.module_name
    cc_out = ctx.actions.declare_file(module_name + "_swig_cc.cc")
    h_out = ctx.actions.declare_file(module_name + "_swig_h.h")
    py_out = ctx.actions.declare_file(module_name + ".py")
    include_dirs = _include_dirs(ctx.attr.deps)
    headers = _headers(ctx.attr.deps)
    args = ["-c++", "-python", "-py3"]
    args += ["-module", module_name]
    args += ["-I" + x for x in include_dirs]
    args += ["-I" + x.dirname for x in ctx.files.swig_includes]
    args += ["-o", cc_out.path]
    args += ["-outdir", py_out.dirname]
    args += ["-oh", h_out.path]

    # Force every swig file we get to %include "swig_exception_forwarding.i".
    modified_source_file = ctx.actions.declare_file(module_name + "_modified.i")
    ctx.actions.run(
        executable = ctx.file.swig_file_appender,
        arguments = [
            "--input",
            ctx.file.source.path,
            "--output",
            modified_source_file.path,
        ],
        inputs = [ctx.file.source],
        outputs = [modified_source_file],
        progress_message = "Appending to %{input}.",
    )

    args.append(modified_source_file.path)
    outputs = [cc_out, h_out, py_out]

    # Depending on the contents of `ctx.file.source`, swig may or may not
    # output a .h file needed by subsequent rules. Bazel doesn't like optional
    # outputs, so instead of invoking swig directly we're going to make a
    # lightweight executable script that first `touch`es the .h file that may
    # get generated, and then execute that. This means we may be propagating
    # an empty .h file around as a "dependency" sometimes, but that's okay.
    # https://stackoverflow.com/questions/73295892/optional-output-from-bazel-action-swig-rule-for-bazel
    swig_script_file = ctx.actions.declare_file("swig_exec.sh")
    ctx.actions.write(
        output = swig_script_file,
        is_executable = True,
        content = "#!/bin/bash\n\nset -e\ntouch " + h_out.path + "\nexec swig \"$@\"",
    )

    ctx.actions.run(
        executable = swig_script_file,
        arguments = args,
        mnemonic = "Swig",
        inputs = [modified_source_file] + headers + ctx.files.swig_includes,
        outputs = outputs,
        progress_message = "SWIGing %{input}.",
    )
    return [
        DefaultInfo(files = depset(direct = [cc_out, py_out])),
        cc_common.merge_cc_infos(cc_infos = [CcInfo(
            compilation_context = cc_common.create_compilation_context(headers = depset(direct = [h_out])),
        )] + [dep[CcInfo] for dep in ctx.attr.deps]),
    ]

_py_swig_gen = rule(
    attrs = {
        "source": attr.label(
            mandatory = True,
            allow_single_file = True,
        ),
        "swig_includes": attr.label_list(
            allow_files = [".i"],
        ),
        "swig_file_appender": attr.label(mandatory = True, allow_single_file = True),
        "deps": attr.label_list(
            allow_files = True,
            providers = [CcInfo],
        ),
        "module_name": attr.string(mandatory = True),
    },
    implementation = _py_swig_gen_impl,
)

def py_wrap_cc(name, source, module_name = None, deps = [], copts = [], **kwargs):
    if module_name == None:
        module_name = name

    python_deps = [
        "@local_config_python//:python_headers",
        "@local_config_python//:python_lib",
    ]

    # First, invoke the _py_wrap_cc rule, which runs swig. This outputs:
    # `module_name.cc`, `module_name.py`, and, sometimes, `module_name.h` files.
    swig_rule_name = "swig_gen_" + name
    _py_swig_gen(
        name = swig_rule_name,
        source = source,
        swig_file_appender = "//third_party/swig_rules:swig_file_appender",
        swig_includes = ["//third_party/swig_rules:swig_includes"],
        deps = deps + python_deps,
        module_name = module_name,
    )

    # Next, we need to compile the `module_name.cc` and `module_name.h` files
    # from the previous rule. The `module_name.py` file already generated
    # expects there to be a `_module_name.so` file, so we name the cc_binary
    # rule this way to make sure that's the resulting file name.
    cc_lib_name = "_" + module_name + ".so"
    native.cc_binary(
        name = cc_lib_name,
        srcs = [":" + swig_rule_name],
        # TODO(jklingner): The "-L" below resolves an issue during the docker
        # build where the linker can't find `-lpython3.9`. I feel like this
        # should be comvered by the @local_config_python extra_deps. To do:
        # figure out why not.
        linkopts = ["-dynamic", "-L/usr/local/lib/"],
        linkshared = True,
        deps = [":" + swig_rule_name] + python_deps,
    )

    # Finally, package everything up as a python library that can be imported
    # depended on. Note that this rule uses the user-given `name`.
    native.py_library(
        name = name,
        srcs = [":" + swig_rule_name],
        srcs_version = "PY3",
        data = [":" + cc_lib_name],
        imports = ["./"],
    )
