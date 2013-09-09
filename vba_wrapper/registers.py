"""
Houses the Registers wrapper.
"""

from copy import copy

class Registers:
    """
    Python magic for reading and writing the registers.
    """

    order = [
        "pc",
        "sp",
        "af",
        "bc",
        "de",
        "hl",
        "iff",
        "div",
        "tima",
        "tma",
        "tac",
        "if",
        "lcdc",
        "stat",
        "scy",
        "scx",
        "ly",
        "lyc",
        "dma",
        "wy",
        "wx",
        "vbk",
        "hdma1",
        "hdma2",
        "hdma3",
        "hdma4",
        "hdma5",
        "svbk",
        "ie",
    ]

    def __init__(self, vba):
        self.vba = vba

    def __setitem__(self, key, value):
        current_registers = self.vba._get_registers()
        current_registers[Registers.order.index(key)] = value
        self.vba._set_registers(current_registers)

    def __getitem__(self, key):
        current_registers = self.vba._get_registers()
        return current_registers[Registers.order.index(key)]

    def __list__(self):
        return self.vba._get_registers()

    def _get_register(id):
        def constructed_func(self, id=copy(id)):
            return self.vba._get_registers()[id]
        return constructed_func

    def _set_register(id):
        def constructed_func(self, value, id=copy(id)):
            current_registers = self.vba._get_registers()
            current_registers[id] = value
            self.vba._set_registers(current_registers)
        return constructed_func

    pc = property(fget=_get_register(0), fset=_set_register(0))
    sp = property(fget=_get_register(1), fset=_set_register(1))
    af = property(fget=_get_register(2), fset=_set_register(2))
    bc = property(fget=_get_register(3), fset=_set_register(3))
    de = property(fget=_get_register(4), fset=_set_register(4))
    hl = property(fget=_get_register(5), fset=_set_register(5))
    iff = property(fget=_get_register(6), fset=_set_register(6))
    div = property(fget=_get_register(7), fset=_set_register(7))
    tima = property(fget=_get_register(8), fset=_set_register(8))
    tma = property(fget=_get_register(9), fset=_set_register(9))
    tac = property(fget=_get_register(10), fset=_set_register(10))
    _if = property(fget=_get_register(11), fset=_set_register(11))
    lcdc = property(fget=_get_register(12), fset=_set_register(12))
    stat = property(fget=_get_register(13), fset=_set_register(13))
    scy = property(fget=_get_register(14), fset=_set_register(14))
    scx = property(fget=_get_register(15), fset=_set_register(15))
    ly = property(fget=_get_register(16), fset=_set_register(16))
    lyc = property(fget=_get_register(17), fset=_set_register(17))
    dma = property(fget=_get_register(18), fset=_set_register(18))
    wy = property(fget=_get_register(19), fset=_set_register(19))
    wx = property(fget=_get_register(20), fset=_set_register(20))
    vbk = property(fget=_get_register(21), fset=_set_register(21))
    hdma1 = property(fget=_get_register(22), fset=_set_register(22))
    hdma2 = property(fget=_get_register(23), fset=_set_register(23))
    hdma3 = property(fget=_get_register(24), fset=_set_register(24))
    hdma4 = property(fget=_get_register(25), fset=_set_register(25))
    hdma5 = property(fget=_get_register(26), fset=_set_register(26))
    svbk = property(fget=_get_register(27), fset=_set_register(27))
    ie = property(fget=_get_register(28), fset=_set_register(28))

    def __repr__(self):
        spacing = "\t"
        output = "Registers:\n"
        registroids = self.vba._get_registers()
        for (id, each) in enumerate(self.order):
            output += spacing + each + " = " + hex(registroids[id])
            output += "\n"
        return output
