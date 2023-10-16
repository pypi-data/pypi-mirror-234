###############################################################################
# (c) Copyright 2013-2023 CERN                                                #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""
Simple script to be used in CMake launcher rules.

A launcher rule defined as

   set_property(GLOBAL PROPERTY RULE_LAUNCH_COMPILE "lbn-wrapcmd <CMAKE_CURRENT_BINARY_DIR> <TARGET_NAME>")

produces log files like SubDir/1234-TargetName-abcd-build.log for each compile command.
"""

import os
import sys
from hashlib import md5
from subprocess import PIPE, STDOUT, Popen
from time import time

try:
    from shlex import quote
except ImportError:  # Python2
    from pipes import quote


def main():
    if len(sys.argv) < 4:
        exit(
            "error: wrong number of arguments.\n"
            "Usage: {} current_binary_dir target command [args ...]".format(
                os.path.basename(sys.argv[0])
            )
        )

    current_binary_dir = sys.argv[1]
    target = sys.argv[2]

    cmd = sys.argv[3:]
    cmd_line = " ".join(quote(a) for a in cmd).encode()
    cmd_hash = md5(cmd_line).hexdigest()[:32]
    logfile = os.path.join(
        current_binary_dir,
        "{}-{}-{}-build.log".format(int(time() * 1e9), target, cmd_hash),
    )

    if not os.path.isdir(current_binary_dir):
        os.makedirs(current_binary_dir)
    with open(logfile, "wb") as f:
        f.write(b"\033[0;32m(")
        f.write(current_binary_dir.encode())
        f.write(b")$ ")
        f.write(cmd_line)
        f.write(b"\033[0m\n")

        # cat is used for merging, we do not need to capture the output
        kwargs = dict(stdout=PIPE, stderr=STDOUT) if cmd[0] != "cat" else {}
        proc = Popen(cmd, **kwargs)
        stdout, _ = proc.communicate()
        if stdout:
            f.write(stdout)
            sys.stdout.buffer.write(stdout)
        if proc.returncode:
            f.write(b"\033[0;31m[command exited with ")
            f.write(str(proc.returncode).encode())
            f.write(b"]\033[0m\n")
        sys.exit(proc.returncode)
