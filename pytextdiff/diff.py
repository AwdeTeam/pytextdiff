"""
diff
====================================================================================================

Diff object which can be applied to text.

----------------------------------------------------------------------------------------------------

**Created**
    2019-07-13
**Updated**
    2019-07-13 by Darkar
**Author**
    Darkar
**Copyright**
    This software is licensed under GPL3, see LICENSE for details.
"""

class Diff:
    """
    A Diff can be applied to a string to modify it or to another diff to combine
    Diffs are immutable.
    Diffs are _not_ communtitive.
    """

    def __init__(self, changes):
        self._changes = changes # List of triplets (word, index, is_addition)

    def apply(self, string):
        """ Modify the string according to the diff """
        words = string.split(" ")

        for word, index, is_add in self._changes:
            if is_add:
                words.insert(index, word)
            else:
                del words[index]

        return " ".join(words)

    def invert(self):
        """ Invert the diff so that it undoes itself """
        invdiff = Diff([[word, index, not is_add] for word, index, is_add in self._changes[::-1]])
        return invdiff

    def concat(self, diff):
        """ Concatenate this diff with another in-order """
        return Diff(self._changes + diff._changes)

    def to_dict(self):
        """ Generate a dictionary representation of this diff """
        return {"diff" : [[word, index, is_add] for word, index, is_add in self._changes]}

    @classmethod
    def from_dict(cls, dct):
        """ Generate a diff from the dictionary """
        return Diff(dct["diff"])
