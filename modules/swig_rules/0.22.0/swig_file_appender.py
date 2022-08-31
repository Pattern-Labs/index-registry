#!/usr/bin/python3
########################### PATTERN LABS NOTICE START ###########################
# Copyright 2022 (C) Pattern Labs, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
############################ PATTERN LABS NOTICE END ############################

"""This file is a simple script which adds LINE_TO_APPEND to an input SWIG file.

This line will be added immediately after the first %module line, if it exists,
or at the beginning of the file if it does not.
"""

import argparse
import pathlib
import re

LINE_TO_APPEND = '%include "swig_exception_forwarding.i"\n'

parser = argparse.ArgumentParser()

parser.add_argument(
    "-i",
    "--input",
    help="Input SWIG (.i) file path.",
    type=pathlib.Path,
    required=True,
    dest="input_path",
)
parser.add_argument(
    "-o",
    "--output",
    help="Output modified SWIG file path.",
    type=pathlib.Path,
    required=True,
    dest="output_path",
)

args = parser.parse_args()

module_line_regex = re.compile(r"^%module.*?$")

module_line = -1
with open(args.input_path, "r") as input_file:
    for line_number, line in enumerate(input_file):
        if module_line_regex.match(line):
            module_line = line_number
            break

line_written = False
with open(args.input_path, "r") as input_file, open(
    args.output_path, "w"
) as output_file:
    for line_number, line in enumerate(input_file):
        if not line_written and (line_number > module_line):
            output_file.write(LINE_TO_APPEND)
            line_written = True
        output_file.write(line)
