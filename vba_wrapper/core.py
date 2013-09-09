"""
vba automation using ctypes
"""

import ctypes

import exceptions
import registers
import cheat

def _load_library_vba():
    """
    Use ctypes to load VBA.
    """
    # TODO: don't use a relative path here
    lib = ctypes.cdll.LoadLibrary("./src/clojure/.libs/libvba.so")
    return lib

def _ctypes_make_list(l, base):
    """
    Makes a list of const char pointers.
    """
    array = (base * len(l))()
    array[:] = l
    return array

class VBA(object):
    """
    VBA wrapper.

    Call the constructor only once per process.

    Note that only one instance of the emulator can be running at any given
    time.
    """

    register_count = 29

    button_masks = {
        "a": 0x0001,
        "b": 0x0002,
        "r": 0x0010,
        "l": 0x0020,
        "u": 0x0040,
        "d": 0x0080,
        "select":   0x0004,
        "start":    0x0008,
        "restart":  0x0800,
        "listen":       -1, # what?
    }

    def __init__(self, rom_path):
        """
        Start the emulator.

        @param rom_path: path to .gb or .gbc file
        """

        # load the library
        self._vba = _load_library_vba()

        self.registers = registers.Registers(self)
        self.cheats = cheat.CheatVBA(self)

        # sometimes ctypes needs some help
        self.setup_ctypes()

        # boot up the emulator
        self.start_emulator(rom_path)

    def setup_ctypes(self):
        """
        ctypes doesn't always know how to pass data around.
        """
        # cache this value and treat it as a constant plz
        self.MAX_SAVE_SIZE = self._get_max_save_size()

        # get_state returns type ctype.c_char_p
        self._vba.get_state.restype = ctypes.POINTER(ctypes.c_char * self.MAX_SAVE_SIZE)

    def start_emulator(self, rom_path):
        """
        Boot up the emulator.
        """
        argv = ["vba-rlm", rom_path]
        return self._vba.main(2, _ctypes_make_list(argv, ctypes.c_char_p))

    def end_emulator(self):
        """
        dunno if this is absolutely necessary
        """
        self._vba.shutdown()

    def shutdown(self):
        """
        just an alias for end_emulator
        """
        self.end_emulator()

    def run(self):
        """
        Advance the state of the emulator until the user presses f12.
        """
        self._vba.step_until_f12()

    def step(self, keymask=0, count=1):
        """
        Advance the state of the emulator by a single "step".

        @param keymask: which buttons to hold (int)
        @param count: how many steps to make?
        """
        if count <= 0:
            raise exceptions.VBAWrapperException("count must be a positive integer")

        while count > 0:
            self._vba.emu_step(keymask)

            count = count - 1

    def tick(self):
        """
        VBA has a function called tick, dunno how it differs from step.
        """
        self._vba.emu_tick()

    def get_current_buttons(self):
        """
        Get an integer representing the current button presses.
        """
        return self._vba.get_current_buttons()

    @staticmethod
    def button_combine(buttons):
        """
        Combines multiple button presses into an integer.

        This is used when sending a keypress to the emulator.
        """
        result = 0

        # String inputs need to be cleaned up so that "start" doesn't get
        # recognized as "s" and "t" etc..
        if isinstance(buttons, str):
            if "restart" in buttons:
                buttons = buttons.replace("restart", "")
                result |= VBA.button_masks["restart"]
            if "start" in buttons:
                buttons = buttons.replace("start", "")
                result |= VBA.button_masks["start"]
            if "select" in buttons:
                buttons = buttons.replace("select", "")
                result |= VBA.button_masks["select"]

            # allow for the "a, b" and "a b" formats
            if ", " in buttons:
                buttons = buttons.split(", ")
            elif " " in buttons:
                buttons = buttons.split(" ")

        if isinstance(buttons, list):
            if len(buttons) > 9:
                raise exceptions.VBAButtonException("can't combine more than 9 buttons at a time")

        for each in buttons:
            result |= VBA.button_masks[each]

        return result

    def press(self, buttons, hold=10, after=1):
        """
        Press a button. Hold the buttonpress for holdsteps number of steps.
        The after parameter is how many steps after holding, with no
        buttonpresses.
        """
        if hasattr(buttons, "__len__"):
            number = self.button_combine(buttons)
        else: # elif isinstance(buttons, int):
            number = buttons

        # hold the button
        for stepnum in range(0, hold):
            self.step(number)

        # clear the buttonpress
        if after > 0:
            for stepnum in range(0, after):
                self.step(0)

    def get_screen(self):
        """
        Returns a boolean representing the status of showScreen.
        """
        return ctypes.c_int.in_dll(self._vba, "showScreen").value == 1

    def set_screen(self, status):
        """
        Set the showScreen variable to "True" by passing 1 and "False" by
        passing 0.
        """
        self._vba.set_showScreen(int(status))

    def enable_screen(self):
        """
        Set showScreen to True.
        """
        self.set_screen(1)

    def disable_screen(self):
        """
        Set showScreen to False.
        """
        self.set_screen(0)

    def get_rom_bank(self):
        """
        gbDataMBC3.mapperROMBank
        """
        return self._vba.get_rom_bank()

    def write_memory_at(self, address, value):
        """
        Write some number at an address.
        """
        self._vba.write_memory_at(address, value)

    def read_memory_at(self, address):
        """
        Read from memory.
        """
        return self._vba.read_memory_at(address)

    def _get_state(self):
        """
        Get a copy of the current emulator state. Might be gzipped?
        """
        buf = (ctypes.c_char * self.MAX_SAVE_SIZE)()
        self._vba.get_state(buf, self.MAX_SAVE_SIZE)
        return bytearray(buf.raw)

    def _set_state(self, state):
        """
        Set the state of the emulator.
        """
        #buf =  _ctypes_make_list(str(state), ctypes.c_char)
        buf = (ctypes.c_char * self.MAX_SAVE_SIZE)()
        buf[:] = str(state)
        self._vba.set_state(buf, self.MAX_SAVE_SIZE)

    state = property(_get_state, _set_state)

    def _get_memory(self):
        """
        Call the getMemory function. Return a bytearray.
        """
        buf = (ctypes.c_int32 * 0x10000)()
        self._vba.get_memory(buf)
        return bytearray(list(buf))

    def _set_memory(self, memory):
        """
        Set the emulator's memory to these bytes.
        """
        #buf = (ctypes.c_int32 * len(memory))()
        #buf[:] = memory
        buf =  _ctypes_make_list(memory, ctypes.c_int32)
        self._vba.set_memory(buf)

    memory = property(_get_memory, _set_memory)

    def _get_ram(self):
        """
        32768 bytes of RAM
        """
        buf = (ctypes.c_int32 * self.ram_size)()
        self._vba.get_ram(buf)
        return bytearray(list(buf))

    ram = property(_get_ram)

    def _get_wram(self):
        """
        WRAM only.
        """
        buf = (ctypes.c_int32 * 0x8000)()
        self._vba.get_wram(buf)
        return bytearray(list(buf))

    wram = property(_get_wram)

    def _get_vram(self):
        """
        VRAM only.
        """
        buf = (ctypes.c_int32 * 0x4000)()
        self._vba.get_vram(buf)
        return bytearray(list(buf))

    vram = property(_get_vram)

    def _get_registers(self):
        """
        Get the current register values.
        """
        # 29 registers
        buf = (ctypes.c_int32 * self.register_count)()
        self._vba.get_registers(buf)
        return list(buf)

    def _set_registers(self, registers):
        """
        Set the CPU registers.
        """
        # 29 registers
        buf = (ctypes.c_int32 * self.register_count)()
        buf[:] = registers
        self._vba.set_registers(registers)

    def _get_max_save_size(self):
        return self._vba.get_max_save_size()

    # this isn't the same as the MAX_SAVE_SIZE "constant"
    max_save_size = property(_get_max_save_size)

    def _get_ram_size(self):
        return self._vba.get_ram_size()

    ram_size = property(_get_ram_size)

    def _get_rom_size(self):
        return self._vba.get_rom_size()

    rom_size = property(_get_rom_size)

    def _get_rom(self):
        """
        the game
        """
        buf = (ctypes.c_int32 * self.rom_size)()
        self._vba.get_rom(buf)
        return bytearray(list(buf))

    def _set_rom(self, rom):
        """
        might have to reset?
        """
        buf = (ctypes.c_int32 * self.rom_size)()
        buf[:] = rom
        self._vba.set_rom(buf)

    rom = property(_get_rom, _set_rom)

    def save_png(self, path):
        """
        Save a png screenshot to the file at path.
        """
        self._vba.save_png(path)

    def say_hello(self):
        """
        Write a message to stdout to show that the binding works.
        """
        self._vba.say_hello()
