#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# ByteWeiser - Byte comparison and replacement tool
# Main core module
# Copyright (c) 2024 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# GitHub: https://github.com/urbanware-org/byteweiser
# GitLab: https://gitlab.com/urbanware-org/byteweiser
#

import os
import sys
import pathlib
from datetime import datetime as dt
from . import common
from . import paval as pv


class ByteWeiser:
    """
        Class for the ByteWeiser compare-and-replace process.
    """

    __version__ = common.get_version()

    def __init__(self):
        self.__file_hashes = True
        self.__file_input = None
        self.__file_input_size = 0
        self.__file_output = None
        self.__file_output_size = 0

        self.__buffer_size = 4096
        self.__buffer_size_min = 1
        self.__percent = 0
        self.__second = 0
        self.__simulate = False
        self.__verbose = True

        self.__byte_blocks = 0
        self.__byte_remainder = 0
        self.__replaced_blocks = 0
        self.__replaced_bytes = 0
        self.__untainted_blocks = 0
        self.__untainted_bytes = 0

        self.__chars_busy = ["/", "-", "\\", "|"]
        self.__chars_index = 0
        self.__padding = 0
        self.__timestamp = None

    def compare_and_replace(self, file_input, file_output, buffer_size=4096,
                            simulate=False, verbose=True, progress=True,
                            hashes=True):
        """
            Main function to compare and replace the bytes (or the blocks).
        """
        file_input = os.path.abspath(file_input)
        file_output = os.path.abspath(file_output)
        buffer_size = int(buffer_size)

        if simulate:
            hashes = False  # as the files remain untainted

        pv.path(file_input, "input", True, True)
        pv.path(file_output, "output", True, True)
        pv.intvalue(buffer_size, "buffer size", True, False, False)

        if file_input == file_output:
            raise ValueError("The path of the input and output file must not "
                             "be identical.")

        if buffer_size < self.__buffer_size_min:
            raise ValueError("The minimal buffer size is %s bytes." %
                             str(self.__buffer_size_min))

        self.__replaced_blocks = 0
        self.__replaced_bytes = 0
        self.__untainted_blocks = 0
        self.__untainted_bytes = 0

        self.__file_hashes = hashes
        self.__file_input = file_input
        self.__file_input_size = common.get_file_size(file_input)
        self.__file_output = file_output
        self.__file_output_size = common.get_file_size(file_output)

        self.__buffer_size = buffer_size
        self.__simulate = simulate
        self.__verbose = verbose

        if self.__file_input_size > self.__file_output_size:
            self.__padding = len(str(self.__file_input_size))
        else:
            self.__padding = len(str(self.__file_output_size))

        self.__byte_blocks = int(self.__file_input_size / self.__buffer_size)
        self.__byte_remainder = self.__file_input_size % self.__buffer_size

        if self.__file_input_size < self.__file_output_size:
            raise ValueError("The input file must at least have the same size "
                             "as the output file.")

        if self.__file_hashes and not self.__simulate:
            if self.__verbose:
                print()
                print("Generating file hashes. Please wait.")
            file_input_hash = common.get_sha256sum(self.__file_input)
            file_output_hash = common.get_sha256sum(self.__file_output)
            if file_input_hash == file_output_hash:
                if self.__verbose:
                    print()
                    print("Nothing to do as the input and output file "
                          "already are identical.")
                    print()
                return

        self.print_input_info(progress)

        if verbose:
            self.__timestamp = dt.now()

        fh_input = open(file_input, "rb")
        if simulate:
            fh_output = open(file_output, "rb")
        else:
            fh_output = open(file_output, "r+b")

        pos = 0
        for block in range(self.__byte_blocks):
            data_input = bytearray(b"")
            data_output = bytearray(b"")
            if progress:
                self.print_status(block)

            data_input.extend(fh_input.read(self.__buffer_size))
            data_output.extend(fh_output.read(self.__buffer_size))
            if data_input != data_output:
                fh_output.seek(pos)
                if not simulate:
                    fh_output.write(data_input)
                else:
                    fh_output.seek(pos + self.__buffer_size)
                self.__replaced_blocks += 1
                self.__replaced_bytes += self.__buffer_size
            else:
                self.__untainted_blocks += 1
                self.__untainted_bytes += self.__buffer_size
            pos += self.__buffer_size

        if self.__byte_remainder > 0:
            data_input = bytearray(b"")
            data_output = bytearray(b"")
            data_input.extend(fh_input.read(self.__byte_remainder))
            data_output.extend(fh_output.read(self.__byte_remainder))
            if data_input != data_output:
                fh_output.seek(pos)
                if not simulate:
                    fh_output.write(data_input)
                self.__replaced_blocks += 1
                self.__replaced_bytes += self.__byte_remainder
            else:
                self.__untainted_blocks += 1
                self.__untainted_bytes += self.__byte_remainder

        if not simulate:
            fh_output.truncate()
            pathlib.Path(file_output).touch()
        fh_output.close()
        fh_input.close()

        self.print_output_info(progress)

    def print_input_info(self, progress):
        """
            Print information about the input data.
        """
        if self.__verbose:
            print()
            print("Input file:")
            print()
            print("    File path:          %s" % self.__file_input)
            print("    File size:          %s bytes" %
                  (str(self.__file_input_size).rjust(self.__padding, " ")))
            print()
            print("    Full blocks:        %s %s\t(with buffer size %s)" %
                  (str(self.__byte_blocks).rjust(self.__padding, " "),
                    common.format_string("block", self.__byte_blocks),
                    self.__buffer_size))
            if self.__byte_remainder == 0:
                print("    Remainder:          %s bytes" %
                      ("0".rjust(self.__padding, " ")))
            else:
                print("    Remainder:          %s %s\t(partial block %s)" %
                      (str(self.__byte_remainder).rjust(self.__padding, " "),
                       common.format_string("byte", self.__byte_remainder),
                       str(self.__byte_blocks + 1)))
            print()

            print("Output file:")
            print()
            print("    File path:          %s" % self.__file_output)
            print("    File size:          %s bytes" %
                  str(self.__file_output_size).rjust(self.__padding, " "))
            print()

            if self.__simulate:
                print("ByteWeiser process (simulation):")
            else:
                print("ByteWeiser process:")
            print()
            if not progress:
                sys.stdout.write("    Processing files. Please wait.\r")
                sys.stdout.flush()
            else:
                sys.stdout.write("    Total progress:\r")
                sys.stdout.flush()

    def print_output_info(self, progress):
        """
            Print results after the main process has been finished.
        """
        identical = True    # default value for simulation

        if self.__verbose:
            if self.__byte_blocks == 0:
                percent = self.__percent
            else:
                percent = \
                    float(self.__replaced_blocks) / self.__byte_blocks * 100

            if percent >= 100:
                percent = 100

            self.__percent = percent        # percent value
            percent = ("%.4f" % percent)    # percent string (formatted)

            if progress:
                print(("    Total progress:     %s %% "
                       "(finished, elapsed time: %s)")
                      % (str("100").rjust(self.__padding, " "),
                         (dt.now() - self.__timestamp)))
            else:
                print("    Finished. Elapsed time: %s"
                      % (dt.now() - self.__timestamp))
            print()
            print("    Replaced blocks:    %s %s" %
                  (str(self.__replaced_blocks).rjust(self.__padding, " "),
                   common.format_string("block", self.__replaced_blocks)))
            print("    Replaced bytes:     %s %s\t(%s %%)" %
                  (str(self.__replaced_bytes).rjust(self.__padding, " "),
                   common.format_string("byte", self.__replaced_bytes),
                   percent))
            print()
            print("    Untainted blocks:   %s %s" %
                  (str(self.__untainted_blocks).rjust(self.__padding, " "),
                   common.format_string("block", self.__untainted_blocks)))
            print("    Untainted bytes:    %s %s" %
                  (str(self.__untainted_bytes).rjust(self.__padding, " "),
                   common.format_string("byte", self.__untainted_bytes)))
            print()

            if self.__file_hashes and not self.__simulate:
                print("    Generating file hashes. Please wait.")
                file_input_hash = common.get_sha256sum(self.__file_input)
                file_output_hash = common.get_sha256sum(self.__file_output)

                print()
                if file_input_hash == file_output_hash:
                    identical = True
                    result = "identical"
                    status = "Success"
                else:
                    identical = False
                    result = "not identical"
                    status = "Failure"

                print("    Status:  %s (input and output file are %s)" %
                      (status, result))
                if identical:
                    print("    SHA256:  %s" % file_input_hash)
                print()

            if self.__file_hashes:
                if identical:
                    print("Process successfully completed.")
                else:
                    print("Process completed with errors.")
            else:
                print("Process completed.")
            print()

    def print_status(self, block):
        """
            Print the current progress in percent.
        """
        if self.__verbose:
            ts = dt.now()
            if ts.second > self.__second:
                self.__chars_index = \
                    (self.__chars_index + 1) % len(self.__chars_busy)
                percent = int(float(block) / self.__byte_blocks * 100)
                percent_string = str(percent).rjust(self.__padding, " ")
                sys.stdout.write("    Total progress:     %s %s" %
                                 (percent_string + " %",
                                  self.__chars_busy[self.__chars_index] +
                                  "\r"))
                sys.stdout.flush()
            self.__second = ts.second

# EOF
