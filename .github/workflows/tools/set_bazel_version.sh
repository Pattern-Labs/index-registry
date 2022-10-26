#!/usr/bin/env bash
###############################################################################
# Copyright 2022 Pattern Labs. Confidential and proprietary, do not distribute.
###############################################################################

CURR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
BAZEL_PATH="${CURR_DIR}"/../../../MODULE.bazel
VERSION_TAG=
IFS=''
file=""
parsed_line=""
module_start=0
module_end=0

function show_usage() {
    cat <<EOF
Usage: $0 [options] ...
OPTIONS:
    -h, --help                     Display this help and exit.
    -t --tag <output tag>          Specify the new version tag.
EOF
}

function parse_arguments() {

    while [ $# -gt 0 ]; do
        local opt="$1"
        shift
        case "${opt}" in
            -h | --help)
                show_usage
                exit 1
                ;;
            -t | --tag)
                VERSION_TAG="$1"
                shift
                ;;
            *)
                echo "Unknown option: ${opt}"
                exit 2
                ;;
        esac
    done # End while loop
    if [[ -z ${VERSION_TAG} ]]; then
        show_usage
        echo ""
        echo "ERROR: Must provide a tag"
        exit 1
    fi
}

function parse_line() {
    local line=$1
    local word
    word=$(echo "$line" | awk '{print $1}')
    parsed_line="$line"
    if [[ $word == "module(" && ( $module_start == 0 ) && ( $module_end == 0 ) ]]; then
        module_start=1
    fi
    if [[ $word == ")" && ( $module_start == 1 ) && ( $module_end == 0 ) ]]; then
        module_end=1
    fi
    if [[ $module_start == 1 && $module_end == 0 ]]; then
        if [[ $word == "version" ]]; then
            parsed_line=$'    version = "'"${VERSION_TAG}"$'",'
        fi
    fi
}

function parse_lines(){
    while read -r line; 
        do {
            parse_line "${line}"
            if [[ "${parsed_line}" != '/n' ]]; then 
                file="${file}${parsed_line}"$'\n'
            fi
        }
    done < "$BAZEL_PATH"
}

function write_file(){
    echo "$file" > "$BAZEL_PATH"
    # Remove the last line of the file which is an extra new line. Prevents this
    # from stacking up as we release new versions.
    tail -n 1 "$BAZEL_PATH" | wc -c | xargs -I {} truncate "$BAZEL_PATH" -s -{}
}
function main() {
    parse_arguments "$@"
    parse_lines
    write_file
    echo "$file"
}

main "$@"
