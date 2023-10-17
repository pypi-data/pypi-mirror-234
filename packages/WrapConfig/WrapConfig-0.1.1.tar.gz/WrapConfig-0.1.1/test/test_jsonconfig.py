import unittest
from unittest.mock import patch, mock_open
import json


class TestJSONConfigManager(unittest.TestCase):
    def setUp(self):
        # Setting up a dummy path for tests
        self.dummy_path = "dummy_path.json"
        self.data = {"key": "value"}

    def test_load_existing_file(self):
        from config_manager import JSONConfigManager

        # Mock the open method to return a string of data
        m = mock_open(read_data=json.dumps(self.data))
        with patch("builtins.open", m):
            manager = JSONConfigManager(self.dummy_path)
            manager.load()
            self.assertEqual(manager.data, self.data)

    def test_save_file(self):
        from config_manager import JSONConfigManager

        # Mock the open method and os methods
        m = mock_open()
        with patch("builtins.open", m), patch(
            "os.path.exists", return_value=False
        ), patch("os.makedirs"):
            manager = JSONConfigManager(self.dummy_path)
            manager._data = self.data
            manager.save()

            written_data = "".join(call[0][0] for call in m().write.call_args_list)

            self.assertEqual(json.dumps(self.data, indent=4), written_data)
