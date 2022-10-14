#!/bin/bash
########################### PATTERN LABS NOTICE START ###########################
# Copyright 2022 (C) Pattern Labs, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
############################ PATTERN LABS NOTICE END ############################
CURR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
file=""

function show_usage() {
    cat <<EOF
Usage: $0 <dependency> <version>
EOF
}

dependency="$1"
version="$2"

if [[ "${dependency}" == "" ]]; then
    show_usage
    echo ""
    echo "ERROR: Dependency is blank."
    exit 1
fi

if [[ "${version}" == "" ]]; then
    show_usage
    echo ""
    echo "ERROR: Version is blank."
    exit 1
fi

bazel_path="${CURR_DIR}"/dependent/MODULE.bazel
while read -r line;
do {
    if [[ $line == *"bazel_dep"* ]]; then # This line is a bazel dependency.
        if [[ $line == *"${dependency}"* ]]; then # This dependency is the module being updated.
            line="bazel_dep(name = "'"'"${dependency}"'"'", version = "'"'"${version}"'"'")"
        fi
    fi
    file="${file}${line}"'\n'
}
done < "$bazel_path"

echo "$file" > "$bazel_path"
# Remove the last line of the file which is an extra new line. Prevents this
# from stacking up as we release new versions.
tail -n 1 "$bazel_path" | wc -c | xargs -I {} truncate "$bazel_path" -s -{}