"""
All the really important tests
"""

import unittest
import mock

import vba_wrapper

class CoreTests(unittest.TestCase):
    @mock.patch("vba_wrapper.core.VBA.start_emulator")
    @mock.patch("vba_wrapper.core.VBA.setup_ctypes")
    @mock.patch("vba_wrapper.core.cheat.CheatVBA")
    @mock.patch("vba_wrapper.core.registers.Registers")
    @mock.patch("vba_wrapper.core._load_library_vba")
    def test_constructor_calls(self, mock_load_library_vba, mock_registers, mock_cheat, mock_setup_ctypes, mock_start_emulator):
        vba = vba_wrapper.core.VBA("/tmp/baserom.gbc")

        self.assertTrue(mock_load_library_vba.called)
        self.assertTrue(mock_setup_ctypes.called)
        self.assertTrue(mock_start_emulator.called)

    def test_button_combine(self):
        button_combine = vba_wrapper.core.VBA.button_combine

        # a and b
        self.assertEqual(0x0001 | 0x0002, button_combine("ab"))

        # a and up
        self.assertEqual(0x0001 | 0x0040, button_combine("au"))

        # b and left
        self.assertEqual(0x0002 | 0x0020, button_combine("bl"))

if __name__ == "__main__":
    unittest.main()
