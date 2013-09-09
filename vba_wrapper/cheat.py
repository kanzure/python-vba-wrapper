"""
Just some extra functions for programmatically cheating with VBA.
"""

class CheatVBA(object):
    """
    Track and apply cheats on the emulator.
    """

    # TODO: there is a gbCheat struct in src/gb/gbCheats.h and it would be nice
    # to have this exposed to the python layer. This would allow for directly
    # manipulating the cheat list instead of tracking ids or whatever (I don't
    # even know how anyone was expected to use that particular API). There's a
    # way to use ctypes to create that struct in python.

    def __init__(self, vba):
        """
        Setup a cheat context on this VBA emulator.
        """
        self.vba = vba

    def load_gameshark_file(self, path):
        """
        Load a gameshark file and setup cheat codes.
        """
        return self.vba._vba.cheat_read_gameshark_file(path)

    def _get_cheat_count(self):
        """
        VBA tracks how many cheats have been put into the system.
        """
        return self.vba._vba.get_cheat_count()

    count = property(_get_cheat_count)

    def add_gameshark(self, code, description):
        """
        Add a gameshark cheat code.
        """
        self.vba._vba.cheat_add_gameshark(code, description)

    def add_gamegenie(self, code, description):
        """
        Add a gamegenie cheat code.
        """
        self.vba._vba.cheat_add_gamegenie(code, description)

    def enable(self, id):
        self.vba._vba.cheat_enable(id)

    def disable(self, id):
        self.vba._vba.cheat_disable(id)

    def remove(self, id):
        self.vba._vba.cheat_remove(id)

    def remove_all(self):
        self.vba._vba.cheat_remove_all()
