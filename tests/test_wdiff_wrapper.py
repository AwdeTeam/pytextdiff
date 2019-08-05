"""
test diff
====================================================================================================

Testing the behavior of the wdiff_wrapper

----------------------------------------------------------------------------------------------------

**Created**
    2019-07-28
**Updated**
    2019-08-04 by WildfireXIII
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
        (
            "The [-short-] {+quick+} brown fox jumped over the lazy [-dog.\r\nNew-] {+dog.\r\nRed leather yellow leather\r\nUnique New+} York [-Sand-]",
            [
                ["short", 1, False],
                ["quick", 1, True],
                ["dog.\r\nNew", 8, False],
                ["dog.\r\nRed leather yellow leather\r\nUnique New", 8, True],
                ["Sand", 14, False],
            ]
        ),
        (
            "[-the-]{+The+} quick brown fox jumped over the lazy dog",
            [
                ["the", 0, False],
                ["The", 0, True]
            ]
        ),
    ],
)
def test_parse_wdiff_output(cmd_output, expected_changes):
    changes = wdiff_wrapper.parse_wdiff_output(cmd_output)
    assert changes == expected_changes


