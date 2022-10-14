#!/bin/bash
########################### PATTERN LABS NOTICE START ###########################
# Copyright 2022 (C) Pattern Labs, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
############################ PATTERN LABS NOTICE END ############################
CURR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
dependents=()

function show_usage() {
    cat <<EOF
Usage: $0 <module> <version>
EOF
}

module="$1"
version="$2"

if [[ "${module}" == "" ]]; then
    show_usage
    echo ""
    echo "ERROR: Module is blank."
    exit 1
fi

if [[ "${version}" == "" ]]; then
    show_usage
    echo ""
    echo "ERROR: Version is blank."
    exit 1
fi

for f in "${CURR_DIR}"/../../../modules/*
do
    [[ -e "$f" ]] || break  # Handle the case of no modules.
    if [ -d "${f}" ] ; then # This is a module folder.
        current_module=$(basename "${f}")
        for v in "${f}"/*
        do
            if [[ -d ${v} ]]; then # This is a version folder.
                current_version=$(basename "${v}")
                bazel_path="${v}"/MODULE.bazel
                while read -r line; 
                do {
                    if [[ $line == *"bazel_dep"* ]]; then # This line is a bazel dependency.
                        if [[ $line == *"${module}"* ]]; then # This dependency is the module being updated.
                            if [[ $line != *"${version}"* ]]; then # This dependency does not match the module version.
                                dependents+=( "${current_module}/${current_version}" ) # Add the dependent and version.
                            fi
                        fi
                    fi
                }
                done < "$bazel_path"
            fi
        done
    fi
done

echo "${dependents[*]}"