"""
Make sure the exceptions are still raised and useful.
"""

import unittest
import mock

import vba_wrapper

class ExceptionsTests(unittest.TestCase):
    @mock.patch("vba_wrapper.core.VBA.start_emulator")
    @mock.patch("vba_wrapper.core.VBA.setup_ctypes")
    @mock.patch("vba_wrapper.core.cheat.CheatVBA")
    @mock.patch("vba_wrapper.core.registers.Registers")
    @mock.patch("vba_wrapper.core._load_library_vba")
    def test_step_raises_exception(self, mock_load_library_vba, mock_registers, mock_cheat, mock_setup_ctypes, mock_start_emulator):
        vba = vba_wrapper.core.VBA("/tmp/baserom.gbc")

        with self.assertRaises(vba_wrapper.exceptions.VBAWrapperException):
            vba.step(count=0)

if __name__ == "__main__":
    unittest.main()
