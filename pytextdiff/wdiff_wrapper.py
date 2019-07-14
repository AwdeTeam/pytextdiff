"""
wdiff_wrapper
====================================================================================================

Functions to handle interfacing with the wdiff command line utility.

----------------------------------------------------------------------------------------------------

**Created**
    2019-07-13
**Updated**
    2019-07-13 by WildfireXIII
**Author**
    WildfireXIII
**Copyright**
    This software is licensed under GPL3, see LICENSE for details.
"""

import subprocess
from shutil import which
from shlex import split

from pytextdiff.exceptions import WDiffNotFound


def call_wdiff(original_text_file, updated_text_file):
    """
    Call the command line utility.

    Returns the string output from the wdiff command
    """

    # check that the wdiff utility exists
    if which("wdiff") is None:
        raise WDiffNotFound()

    cmd = "wdiff '{0}' '{1}'".format(original_text_file, updated_text_file)

    # run the command and return the output
    cmd_output_b = subprocess.run(split(cmd), stdout=subprocess.PIPE)
    cmd_output = cmd_output_b.stdout.decode('utf-8')
    
    return cmd_output
