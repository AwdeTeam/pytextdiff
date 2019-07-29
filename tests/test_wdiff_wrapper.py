"""
test diff
====================================================================================================

Testing the behavior of the wdiff_wrapper

----------------------------------------------------------------------------------------------------

**Created**
    2019-07-28
**Updated**
    2019-07-28 by WildfireXIII
**Author**
    Darkar
**Copyright**
    This software is licensed uner GPL3, see LICENSE for details
"""

import pytest

from pytextdiff import wdiff_wrapper
from pytextdiff.diff import Diff


@pytest.mark.parametrize(
    "cmd_output, expected_changes",
    [
        (
            "The [-short-] {+quick+} brown fox jumped over the lazy dog.\n {+Red leather yellow leather\n Unique+} New York [-Sand-]",
            [
                ["short", 1, False],
                ["quick", 1, True],
                ["Red leather yellow leather\n Unique", 9, True],
                ["Sand", 16, False],
            ]
        ),
    ],
)
def test_parse_wdiff_output(cmd_output, expected_changes):
    changes = wdiff_wrapper.parse_wdiff_output(cmd_output)
    assert changes == expected_changes


@pytest.mark.parametrize(
        "cmd_output, input_string, expected_output_string",
        [
            (
                "The [-short-] {+quick+} brown fox jumped over the lazy dog.\n {+Red leather yellow leather\n Unique+} New York [-Sand-]",
                "The short brown fox jumped over the lazy dog.\n New York Sand",
                "The quick brown fox jumped over the lazy dog.\n Red leather yellow leather\n Unique New York"
            ),
        ],
)
def test_parse_wdiff_output_applies(cmd_output, input_string, expected_output_string):
    changes = wdiff_wrapper.parse_wdiff_output(cmd_output)
    diff = Diff(changes)

    
    assert diff.apply(input_string) == expected_output_string
