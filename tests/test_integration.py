"""
test integration
====================================================================================================

Test the wdiff wrapper and the diff object

----------------------------------------------------------------------------------------------------

**Created**
    2019-08-04
**Updated**
    2019-08-04 by Darkar
**Author**
    Darkar
**Copyright**
    This software is licensed under GPL3, see LICENSE for details
"""

import pytest

from pytextdiff.diff import Diff
from pytextdiff import wdiff_wrapper

def test_insertion():
    """ Test the basic behavior of finding a diff and applying it """
    pre_string = "Hey, everybody! Somebody 'mattress' to Mr Lambert - *twice*!"
    post_string = "Hey, everybody! Somebody said 'mattress' to Mr Lambert - *twice*!"
    diff = wdiff_wrapper.run_wdiff(pre_string, post_string)
    assert diff.apply(pre_string) == post_string

def test_insert_first():
    """ Test inserting the first word """
    pre_string = "everybody! Somebody 'mattress' to Mr Lambert - *twice*!"
    post_string = "Hey, everybody! Somebody said 'mattress' to Mr Lambert - *twice*!"
    diff = wdiff_wrapper.run_wdiff(pre_string, post_string)
    assert diff.apply(pre_string) == post_string

def test_removal():
    """ Test the basic behavior of finding a diff and applying it """
    pre_string = "The deceased, Mr Apricot, jam is now 'elpless."
    post_string = "The deceased, Mr Apricot, is now 'elpless."
    diff = wdiff_wrapper.run_wdiff(pre_string, post_string)
    assert diff.apply(pre_string) == post_string

def test_remove_first():
    """ Test the basic behavior of finding a diff and applying it """
    pre_string = "The deceased, Mr Apricot, is now 'elpless."
    post_string = "deceased, Mr Apricot, is now 'elpless."
    diff = wdiff_wrapper.run_wdiff(pre_string, post_string)
    assert diff.apply(pre_string) == post_string

def test_invert_first():
    """ Test the basic behavior of finding a diff and applying it """
    pre_string = "The deceased, Mr Apricot, is now 'elpless."
    post_string = "deceased, Mr Apricot, is now 'elpless."
    diff = wdiff_wrapper.run_wdiff(pre_string, post_string)
    assert diff.invert().apply(post_string) == pre_string

def test_multi_add():
    """ Test that diff is able to add multiple words in a single change """
    pre_string = "The short brown fox jumped over the lazy dog. New York Sand"
    post_string = "The quick brown fox jumped over the lazy dog. " +\
            "Red leather yellow leather Unique New York"
    diff = wdiff_wrapper.run_wdiff(pre_string, post_string)
    assert diff.apply(pre_string) == post_string

def test_multi_space():
    """ Test that diff is able to handle multiple spaces """
    pre_string = "Hey,  everybody! Somebody 'mattress' to Mr Lambert!"
    post_string = "Hey,  everybody! Somebody said 'mattress' to Mr Lambert!"
    diff = wdiff_wrapper.run_wdiff(pre_string, post_string)
    assert diff.apply(pre_string) == post_string
    
def test_leading_space():
    """ Test that diff is able to handle multiple spaces """
    pre_string = " Hey, everybody! Somebody 'mattress' to Mr Lambert!"
    post_string = " Hey, everybody! Somebody said 'mattress' to Mr Lambert!"
    diff = wdiff_wrapper.run_wdiff(pre_string, post_string)
    assert diff.apply(pre_string) == post_string

def test_add_space():
    """ Test that diff is able to add a space """
    pre_string = "Hey, everybody! Somebody 'mattress' to Mr Lambert!"
    post_string = "Hey,  everybody! Somebody said 'mattress' to Mr Lambert!"
    diff = wdiff_wrapper.run_wdiff(pre_string, post_string)
    assert diff.apply(pre_string) == post_string
    
def test_remove_space():
    """ Test that diff is able to remove a space """
    pre_string = "Hey,  everybody! Somebody 'mattress' to Mr Lambert!"
    post_string = "Hey, everybody! Somebody said 'mattress' to Mr Lambert!"
    diff = wdiff_wrapper.run_wdiff(pre_string, post_string)
    assert diff.apply(pre_string) == post_string
    
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
