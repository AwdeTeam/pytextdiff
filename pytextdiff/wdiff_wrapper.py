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


    # ---- parse output for removals ----

    # find each instance of a removal starting delimiter
    removal_starts = output.split("[-")

    word_offset = 0

    for removal_start_section in removal_starts:
        # ensure begins with delimiter
        if removal_start_section[:2] != "[-":
            word_offset += len(removal_start_section.split(" "))
            continue

        # find the index of the end delimiter
        end_index = removal_start_section.index("-]")
        remove_section = removal_start_section[2:end_index]

        change = (remove_section, word_offset, "-")
        changes.append(change)

        # recalculate word offset
        word_offset += len(removal_start_section.split(" "))


    # ---- parse output for additions ----

    addition_starts = output.split("{+")

    # find each instance of a addition starting delimiter
    addition_starts = output.split("{+")

    word_offset = 0

    for addition_start_section in addition_starts:
        # ensure begins with delimiter
        if addition_start_section[:2] != "{+":
            word_offset += len(addition_start_section.split(" "))
            continue

        # find the index of the end delimiter
        end_index = addition_start_section.index("+}")
        remove_section = addition_start_section[2:end_index]

        change = (remove_section, word_offset, "+")
        changes.append(change)

        # recalculate word offset
        word_offset += len(addition_start_section.split(" "))


    # ---- offset adjustment ----
    # since word removals affect actual word indices, do a second pass through of the changes and
    # update the indices to account for prior changes

    # sort changes by the word offset
    changes = sorted(changes, key=lambda tup: tup[1])

    # for every removal in the change, take the number of words in it and subtract it from all
    # later changes' word offsets
    for i in range(0, len(changes)):
        change = changes[i]
        if change[2] == "-": # if it's a removal
            change_word_count = len(change[0].split(" "))
            for j in range(i+1, len(changes)): # subtract word count from all later changes
                future_change = changes[j]
                future_change[1] -= change_word_count

    return changes
