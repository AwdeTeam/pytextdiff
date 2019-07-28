"""
test diff
====================================================================================================

Testing the behavior of diff objects.

----------------------------------------------------------------------------------------------------

**Created**
    2019-07-28
**Updated**
    2019-07-28 by Darkar
**Author**
    Darkar
**Copyright**
    This software is licensed uner GPL3, see LICENSE for details
"""

from pytextdiff.diff import Diff

def test_apply():
    """ Test the basic behavior of applying a diff to a string """
    string = "Hey, everybody! Somebody 'mattress' to Mr Lambert - *twice*!"
    diff = Diff([(3, True, "said")])
    assert diff.apply(string) == "Hey, everybody! Somebody said 'mattress' to Mr Lambert - *twice*!"

