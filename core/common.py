#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ============================================================================
# ByteWeiser - Byte comparison and replacement tool
# Common core module
# Copyright (C) 2021 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# GitHub: https://github.com/urbanware-org/byteweiser
# GitLab: https://gitlab.com/urbanware-org/byteweiser
# ============================================================================

__version__ = "1.0.2"

import hashlib


def get_file_size(file_path):
    """
        Get the size of a file in bytes.
    """
    input_file = open(file_path, "rb")
    input_file.seek(0, 2)
    file_size = input_file.tell()
    input_file.close()

    return int(file_size)


def get_sha256sum(file_path):
    """
        Get the SHA256 hash from a file.
    """
    input_file = open(file_path, 'rb')
    data = input_file.read()
    hlib = hashlib.sha256()
    hlib.update(data)
    sha256_hash = hlib.hexdigest()
    return sha256_hash


def get_version():
    """
        Return the version of this module.
    """
    return __version__


# EOF
