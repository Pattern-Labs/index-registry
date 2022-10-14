#!/bin/bash
########################### PATTERN LABS NOTICE START ###########################
# Copyright 2022 (C) Pattern Labs, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
############################ PATTERN LABS NOTICE END ############################
function show_usage() {
    cat <<EOF
Usage: $0 <version>
EOF
}

version="$1"

if [[ "${version}" == "" ]]; then
    show_usage
    echo ""
    echo "ERROR: Version is blank."
    exit 1
fi
IFS='.' read -ra NUMS <<< "$version"    #Convert string to array
if [[ "${version}" =~ [0-9]+.[0-9]+.[0-9]+ ]]; then # Is Valid Version.
    major=${NUMS[0]}
    minor=${NUMS[1]}
    patch=$((NUMS[2]+1))
    new_version="${major}.${minor}.${patch}"
    echo "$new_version"
else
    exit 1
fi