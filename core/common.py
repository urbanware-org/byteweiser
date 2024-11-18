#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# ByteWeiser - Byte comparison and replacement tool
# Common core module
# Copyright (c) 2024 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# GitHub: https://github.com/urbanware-org/byteweiser
# GitLab: https://gitlab.com/urbanware-org/byteweiser
#

__version__ = "1.0.2"

import hashlib


def format_string(string, number):
    """
        Format string by adding an 's' for plurals.
    """
    if number != 1:
        string += "s"
    else:
        string += " "
    string += " "

    return string


def get_file_size(file_path):
    """
        Get the size of a file in bytes.
    """
    input_file = open(file_path, "rb")
    input_file.seek(0, 2)
    file_size = input_file.tell()
    input_file.close()

    return int(file_size)


def get_sha256sum(file_path, buffer_size=4096):
    """
        Get the SHA256 hash from a file.
    """
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as file:
        for byte_block in iter(lambda: file.read(buffer_size), b""):
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()


def get_version():
    """
        Return the version of this module.
    """
    return __version__

# EOF
