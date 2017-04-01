#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ============================================================================
# ByteWeiser - Byte comparison and replacement tool
# Main script
# Copyright (C) 2017 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# GitHub: https://github.com/urbanware-org/byteweiser
# ============================================================================

import os
import sys

def main():
    from core import clap
    from core import common
    from core import main

    try:
        p = clap.Parser()
    except Exception as e:
        print("%s: error: %s" % (os.path.basename(sys.argv[0]), e))
        sys.exit(1)

    p.set_description("Compare two files and replace different bytes.")
    p.set_epilog("Further information and usage examples can be found " \
                 "inside the documentation file for this script.")

    # Required arguments
    p.add_avalue("-i", "--input-file", "source file where to read the data " \
                 "from", "input_file", None, True)
    p.add_avalue("-o", "--output-file", "destination file where to write " \
                 "data into", "output_file", None, True)

    # Optional arguments
    p.add_avalue("-b", "--buffer-size", "buffer size in bytes", "buffer_size",
                 4096, False)
    p.add_switch("-q", "--quiet", "disable output", "quiet", True, False)
    p.add_switch("-s", "--simulate", "do not change the output file",
                 "simulate", True, False)

    if len(sys.argv) == 1:
        p.error("At least one required argument is missing.")
    elif ("-h" in sys.argv) or ("--help" in sys.argv):
        p.print_help()
        sys.exit(0)
    elif "--version" in sys.argv:
        print(common.get_version())
        sys.exit(0)

    args = p.parse_args()
    try:
        verbose = not args.quiet    
        byteweiser = main.ByteWeiser()
        byteweiser.compare_and_replace(args.input_file, args.output_file,
                                       args.buffer_size, args.simulate,
                                       verbose)
    except Exception as e:
        p.error(e)

if __name__ == "__main__":
    main()

# EOF

