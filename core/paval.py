#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# PaVal - Parameter validation module
# Copyright (C) 2022 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# GitHub: https://github.com/urbanware-org/paval
# GitLab: https://gitlab.com/urbanware-org/paval
#

__version__ = "1.3.0"

import filecmp
import os


def compfile(file_path, name="", list_files=None):
    """
        Compare files to avoid that the same file is given multiple times or
        in different ways (e.g. different name but same content).
    """
    __string(file_path, "%s path" % name, True)

    if list_files is None:
        list_files = []
    elif not list_files:
        __ex("File list is empty (no files to compare with).", True,
             ValueError)
    else:
        for item in list_files:
            if not isinstance(item, list):
                __ex("Every list item must be a sub-list.", True,
                     ValueError)
            if not len(item) == 2:
                __ex("Every sub-list must contain two items.", True,
                     ValueError)

    file_path = os.path.abspath(file_path)
    for item in list_files:
        path_compare = os.path.abspath(str(item[0]))
        name_compare = str(item[1])
        if file_path == path_compare:
            __ex("The %s and the %s file path must not be identical." %
                 (name, name_compare), False, ValueError)
        if os.path.exists(file_path) and os.path.exists(path_compare):
            if filecmp.cmp(file_path, path_compare, 0):
                __ex("The %s and %s file content must not be identical." %
                     (name, name_compare), False, ValueError)


def compstr(input_string, name="", list_strings=None):
    """
        Compare a string with a list of strings and check if it is an item of
        that list.
    """
    __string(input_string, name, False)
    if not list_strings:
        __ex("No %s strings to compare with." % name, True, ValueError)
    if input_string not in list_strings:
        __ex("The %s '%s' does not exist." % (name, input_string), False,
             FileNotFoundError)


def get_version():
    """
        Return the version of this module.
    """
    return __version__


def intrange(value, name="", value_min=None, value_max=None, zero=False):
    """
        Validate an integer range.
    """
    value = __integer(value, "%s value" % name, False)
    if value_min is not None:
        value_min = __integer(value_min, "minimal %s value" % name, True)
        intvalue(value_min, name, True, True, True)
    if value_max is not None:
        value_max = __integer(value_max, "maximal %s value" % name, True)
        intvalue(value_max, name, True, True, True)
    if not zero:
        if value == 0:
            __ex("The %s value must not be zero." % name, False, ValueError)
    if (value_min is not None) and (value_max is not None):
        if value_min > value_max:
            __ex("The maximal %s value must be greater than the minimal "
                 "value." % name, False, ValueError)
        if (value_min == value_max) and (value != value_min):
            __ex("The %s value can only be %s (depending on further range "
                 "further range arguments)." % (name, value_min), False,
                 ValueError)
        if (value < value_min) or (value > value_max):
            __ex("The %s value must be between %s and %s (depending on "
                 "further range arguments)." % (name, value_min, value_max),
                 False, ValueError)
    elif value_min is not None:
        if value < value_min:
            __ex("The %s value must not be less than %s." % (name, value_min),
                 False, ValueError)
    elif value_max is not None:
        if value > value_max:
            __ex("The %s value must not be greater than %s." %
                 (name, value_max), False, ValueError)


def intvalue(value, name="", positive=True, zero=False, negative=False):
    """
        Validate a single integer value.
    """
    value = __integer(value, "%s value" % name, False)
    if not positive:
        if value > 0:
            __ex("The %s value must not be positive." % name, False,
                 ValueError)
    if not zero:
        if value == 0:
            __ex("The %s value must not be zero." % name, False, ValueError)
    if not negative:
        if value < 0:
            __ex("The %s value must not be negative." % name, False,
                 ValueError)


def path(pathname, name="", is_file=False, exists=False):
    """
        Validate a path of a file or directory.
    """
    string(pathname, "%s path" % name, False, None)
    pathname = os.path.abspath(pathname)

    if is_file:
        path_type = "file"
    else:
        path_type = "directory"
    if exists:
        if not os.path.exists(pathname):
            __ex("The given %s %s does not exist." % (name, path_type), False,
                 FileNotFoundError)
        if (is_file and not os.path.isfile(pathname)) or \
           (not is_file and not os.path.isdir(pathname)):
            __ex("The given %s %s path is not a %s." % (name, path_type,
                                                        path_type), False)
    else:
        if os.path.exists(pathname):
            __ex("The given %s %s path already exists." % (name, path_type),
                 False, FileExistsError)


def param_type_list(param_list=[], strict=True):
    """
        Validate parameter types using a list.
    """
    for param in param_list:
        p_value = [param][0][0]  # value
        p_desc = [param][0][1]   # description
        p_type = [param][0][2]   # expected value type

        if not strict:
            if type(p_value) == int and p_type == float:
                # In case a float is expected and an integer is given, convert
                # the integer to float, e.g. '2' to '2.0'
                p_value = float(p_value)

        if p_type is None:
            __ex("Parameter '%s' must not be 'NoneType'." % p_desc, TypeError)

        if not isinstance(p_value, p_type):
            # Quick-and-dirty solution without using regular expressions.
            # Works as expected at least.
            p_type = repr(p_type).split()[1].rstrip(">")

            __ex("Parameter '%s' is not type of %s." % (p_desc, p_type),
                 TypeError)


def string(input_string, name="", wildcards=False, invalid_chars=None):
    """
        Validate a string.
    """
    __string(input_string, name, False)
    if invalid_chars is None:
        invalid_chars = ""
    if not wildcards:
        if ("*" in input_string) or ("?" in input_string):
            __ex("The %s must not contain wildcards." % name, False,
                 ValueError)
    if invalid_chars:
        for char in invalid_chars:
            if char in input_string:
                # Use single quotes by default or double quotes in case the
                # single quotes are the invalid character
                quotes = "'"
                if char == quotes:
                    quotes = "\""

                __ex("The %s contains at least one invalid character "
                     "(%s%s%s)." % (name, quotes, char, quotes), False,
                     ValueError)


def __ex(exception_string, internal=False, exception_type=TypeError):
    """
        Internal method to raise an exception.
    """
    ex = str(exception_string).strip()
    while " " * 2 in ex:
        ex = ex.replace((" " * 2), " ")
    if internal:
        ex = "PaVal: " + ex
    raise exception_type(ex)


def __integer(value, name="", internal=False):
    """
        Internal method for basic integer validation.
    """
    if value is None:
        __ex("The %s is missing." % name, internal, ValueError)
    if value == "":
        __ex("The %s must not be empty." % name, internal, ValueError)
    try:
        value = int(value)
    except ValueError:
        __ex("The %s must be an integer." % name, internal, TypeError)
    return int(value)


def __string(input_string, name="", internal=False):
    """
        Internal method for basic string validation.
    """
    if input_string is None:
        __ex("The %s is missing." % name, internal, ValueError)
    if input_string == "":
        __ex("The %s must not be empty." % name, internal, ValueError)
