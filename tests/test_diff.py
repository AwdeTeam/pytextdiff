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
    string = "The plumage don't enter into it. It's stone dead."
    diff_a = Diff([("spam", 3, True)])
    diff_b = Diff([("plumage", 1, False)])
    diff_cat = diff_a.concat(diff_b)
    altstring = diff_a.apply(string)
    altstring = diff_b.apply(altstring)
    assert diff_cat.apply(string) == altstring

def test_associativity():
    """ Diffs should associate, (A+B)+C=A+(B+C) """
    string = "It's not much of a cheese shop, is it?"
    diff_a = Diff([("not", 1, False)])
    diff_b = Diff([("good", 3, True)])
    diff_c = Diff([("then", 4, True)])
    diff_ab = diff_a.concat(diff_b)
    diff_bc = diff_b.concat(diff_c)
    assert diff_c.apply(diff_ab.apply(string)) == diff_bc.apply(diff_a.apply(string))

def test_identity():
    """ Concatenating a diff with its inversion should be a no-op """
    string = "I'm a lumberjack, and I'm okay. I sleep all night and I work all day."
    diff = Diff([("lumberjack,", 2, False), ("parrot", 6, True), ("spam", 8, True)])
    no_diff = diff.concat(diff.invert())
    assert no_diff.apply(string) == string

def test_serialization():
    """ Test that diffs serialize as expect """
    string = "I want to apologize, humbly, deeply, and sincerely about the fork."
    diff = Diff([("really", 1, True), ("apologize", 4, False)])
    diffdct = diff.to_dict()
    assert Diff.from_dict(diffdct).apply(string) == diff.apply(string)

def test_multi_add():
    """ Test that diff is able to add multiple words in a single change """
    string0 = "The short brown fox jumped over the lazy dog. New York Sand"
    string1 = "The quick brown fox jumped over the lazy dog. " +\
            "Red leather yellow leather Unique New York"
    diff = Diff([
        ["short", 1, False],
        ["quick", 1, True],
        ["Red leather yellow leather Unique", 9, True],
        ["Sand", 16, False]
    ])
    assert diff.apply(string0) == string1

def test_multi_space():
    """ Test that diff is able to handle multiple spaces """
    string = "Hey,  everybody! Somebody 'mattress' to Mr Lambert!"
    diff = Diff([("said", 4, True)])
    assert diff.apply(string) == "Hey,  everybody! Somebody said 'mattress' to Mr Lambert!"
    
def test_leading_space():
    """ Test that diff is able to handle multiple spaces """
    string = " Hey, everybody! Somebody 'mattress' to Mr Lambert!"
    diff = Diff([("said", 4, True)])
    assert diff.apply(string) == " Hey, everybody! Somebody said 'mattress' to Mr Lambert!"
