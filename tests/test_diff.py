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

def test_insertion():
    """ Test the basic behavior of applying a diff to a string """
    string = "Hey, everybody! Somebody 'mattress' to Mr Lambert - *twice*!"
    diff = Diff([("said", 3, True)])
    assert diff.apply(string) == "Hey, everybody! Somebody said 'mattress' to Mr Lambert - *twice*!"

def test_removal():
    """ Test that a diff can remove a word as well as insert one """
    string = "The deceased, Mr Apricot, jam is now 'elpless."
    diff = Diff([("jam", 4, False)])
    assert diff.apply(string) == "The deceased, Mr Apricot, is now 'elpless."

def test_invert():
    """ Test that an inverted diff undoes a change """
    string = "No no no, my fish's name is Eric, Eric the fish. He's an halibut."
    diff = Diff([("no", 1, False), ("salt", 8, True)])
    altstring = diff.apply(string)
    assert diff.invert().apply(altstring) == string

def test_contatenation():
    """ Check that two diffs concatenate correctly """
    pass

def test_associativity():
    """ Diffs should associate """
    string = "It's not much of a cheese shop, is it?"
    pass
