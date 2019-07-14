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
    """

    def __init__(self, additions, subtractions):
        self._additions #A list of ordered pairs (index, word) to add to the text
        self._subtractions #A list of ordered pairs (index, word) to remove from the text
        self._inverted = False

    def apply(self, string):
        """ Modify the string according to the diff """
        words = string.split(" ")

        if self._inverted:
            for index, _ in self.subtractions:
                del words[index]

        for index, word in self._additions:
            words.insert(index, word)

        if not self._inverted:
            for index, _ in self.subtractions:
                del words[index]

        return " ".join(words)

    def invert(self):
        """ Invert the diff so that it undoes itself """
        invdiff = Diff(self._subtractions[::-1], self._additions[::-1])
        invdiff._inverted = not self._inverted

    def concat(self, diff):
        """ Concatenate this diff with another in-order """
        if self._inverted != diff._inverted:
            # I'm not really sure what to do when this happens
            raise NotImplementedError
        conadds = self._additions + diff._additions
        consubs = self._subtractions + diff._subtractions
        condiff = Diff(conadds, consubs)
        condiff._inverted = self._inverted
        return condiff
