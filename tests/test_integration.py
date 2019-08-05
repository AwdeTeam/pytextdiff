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
