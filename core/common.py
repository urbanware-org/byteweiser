#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ============================================================================
# ByteWeiser - Byte comparison and replacement tool
# Common core module
# Copyright (C) 2018 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# GitHub: https://github.com/urbanware-org/byteweiser
# ============================================================================

__version__ = "1.0.2"


def get_file_size(file_path):
    """
        Get the size of a file in bytes.
    """
    input_file = open(file_path, "rb")
    input_file.seek(0, 2)
    file_size = input_file.tell()
    input_file.close()

    return int(file_size)


def get_version():
    """
        Return the version of this module.
    """
    return __version__

# EOF
