"""
exceptions
====================================================================================================

Custom exceptions for when things don't go according to plan

----------------------------------------------------------------------------------------------------

**Created**
    2019-07-13
**Updated**
    2019-07-13 by WildfireXIII
**Author**
    WildfireXIII
**Copyright**
    This software is licensed under GPL3, see LICENSE for details.
"""

class WDiffNotFound(Exception):
    """Raised if the wdiff utility not found in PATH."""
