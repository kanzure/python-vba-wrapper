"""
Library exceptions go here
"""

class VBAWrapperException(Exception):
    """
    Used for exceptions in the python layer that wraps the vba emulator
    library.
    """

class VBAButtonException(VBAWrapperException):
    """
    Used for exceptions related to emulator input.
    """
