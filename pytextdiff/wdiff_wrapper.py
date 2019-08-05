"""
wdiff_wrapper
====================================================================================================

Functions to handle interfacing with the wdiff command line utility.

----------------------------------------------------------------------------------------------------

**Created**
    2019-07-13
**Updated**
    2019-07-27 by WildfireXIII
**Author**
    WildfireXIII
**Copyright**
    This software is licensed under GPL3, see LICENSE for details.
"""

import logging
import subprocess
import os
from shutil import which
from shlex import split

from pytextdiff.exceptions import WDiffNotFound

from pytextdiff import diff


def run_wdiff(original_text, updated_text):
    """
    Takes given text and stores into temporary files to be used by the wdiff utility.

    Returns the Diff object between the two pieces of text.
    """

    # store the text into files
    original_file = "pytextdiff_temp_original_text_file"
    logging.info("Saving original text to file...")
    with open(original_file, 'w') as out_file:
        out_file.write(original_text)

    updated_file = "pytextdiff_temp_updated_text_file"
    logging.info("Saving updated text to file...")
    with open(updated_file, 'w') as out_file:
        out_file.write(updated_text)

    # run wdiff
    output = call_wdiff_cmd(original_file, updated_file)

    # remove temporary files
    logging.info("Removing temporary files...")
    os.remove(original_file)
    os.remove(updated_file)

    # parse changes
    changes = parse_wdiff_output(output)

    diff_obj = diff.Diff(changes)
    return diff_obj


def call_wdiff_cmd(original_text_file, updated_text_file):
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
    removal_starts = output.split(" [-")

    # make sure the first word wasn't a removal (remove the delimiter if so)
    if len(output) > 2 and output[0:2] == "[-":
        removal_starts[0] = removal_starts[0][2:]

    word_offset = 0

    for removal_start_section in removal_starts:
        print("removal loop")
        print(removal_start_section)

        # find the index of the end delimiter
        end_index = 0
        try:
            end_index = removal_start_section.index("-]")
        except ValueError:
            # this was probably the first section before an actual removal because of how split works
            word_offset += len(removal_start_section.split(" "))
            continue

        print(end_index)
        remove_section = removal_start_section[:end_index]

        change = [remove_section, word_offset, False]
        print(change)
        changes.append(change)

        # recalculate word offset
        word_offset += len(removal_start_section.split(" "))


    # ---- parse output for additions ----

    # find each instance of a addition starting delimiter
    addition_starts = output.split(" {+")
    
    # make sure the first word wasn't a removal (remove the delimiter if so)
    if len(output) > 2 and output[0:2] == "{+":
        removal_starts[0] = removal_starts[0][2:]

    word_offset = 0

    for addition_start_section in addition_starts:
        # find the index of the end delimiter
        end_index = 0
        try:
            end_index = addition_start_section.index("+}")
        except ValueError:
            # this was probably the first section before an actual removal because of how split works
            word_offset += len(addition_start_section.split(" "))
            continue

        print(end_index)
        remove_section = addition_start_section[:end_index]

        change = [remove_section, word_offset, True]
        changes.append(change)

        # recalculate word offset
        word_offset += len(addition_start_section.split(" "))


    # ---- offset adjustment ----
    # since word removals affect actual word indices, do a second pass through of the changes and
    # update the indices to account for prior changes

    # sort changes by the word offset
    changes = sorted(changes, key=lambda tup: tup[1])

    # for every removal in the change, take the number of words in it and subtract it from all
    # later changes' word offsets (by offset index, not list position)
    for i in range(0, len(changes)):
        change = changes[i]
        is_addition = change[2]
        change_offset = change[1]
        if not is_addition: # if it's a removal
            change_word_count = len(change[0].split(" "))
            for j in range(i+1, len(changes)): # subtract word count from all later changes (if it comes after change)
                future_change = changes[j]
                if future_change[1] <= change_offset: # it wasn't _actually_ in the future, so skip NOTE: this shouldn't actually happen since sorted by offset
                    continue
                future_change[1] -= change_word_count

    print(changes)
    return changes
