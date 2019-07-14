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

import logging
import subprocess
from shutil import which
from shlex import split

from pytextdiff.exceptions import WDiffNotFound


def call_wdiff(original_text_file, updated_text_file):
    """
    Call the command line utility.

    Returns the string output from the wdiff command.
    """

    # check that the wdiff utility exists
    if which("wdiff") is None:
        raise WDiffNotFound()

    cmd = "wdiff '{0}' '{1}'".format(original_text_file, updated_text_file)
    logging.info("Executing command \"%s\"", cmd)

    # run the command and return the output
    cmd_output_b = subprocess.run(split(cmd), stdout=subprocess.PIPE)
    cmd_output = cmd_output_b.stdout.decode('utf-8')

    return cmd_output


def parse_wdiff_output(output):
    """
    Parses the wdiff command output for all additions and removals.

    Returns the list of tuples for changes.
    """

    changes = []

    # split the output into words (naively by spaces)
    words = output.split(" ")

    building = False # set to True if found an opening delimiter and searching for end delimiter
    building_addition = False
    building_index = 0
    building_phrase = "" # keeps track of a removal or deletion that spans multiple iterations/words

    for word in words:

        del_begin = word.index("[-")
        del_end = word.index("-]")
        add_begin = word.index("{+")
        add_end = word.index("+}")

        if building:
            pass
        else:
            if del_begin != -1: # do we have a delition beginning?
                if del_end != -1: # do we also have a deletion ending?
                    pass
