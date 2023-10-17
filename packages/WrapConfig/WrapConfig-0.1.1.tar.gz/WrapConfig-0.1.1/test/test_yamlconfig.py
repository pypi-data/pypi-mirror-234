import unittest
from unittest.mock import patch, mock_open
import yaml


class TestYAMLConfigManager(unittest.TestCase):
    def setUp(self):
        # Setting up a dummy path for tests
        self.dummy_path = "dummy_path.yaml"
        self.data = {"key": "value"}

    def test_load_existing_file(self):
        from config_manager import YAMLConfigManager

        # Mock the open method to return a string of data
        m = mock_open(
            read_data=yaml.dump(self.data)
        )  # Use yaml.dump() instead of json.dumps()
        with patch("builtins.open", m):
            manager = YAMLConfigManager(self.dummy_path)
            manager.load()
            self.assertEqual(manager.data, self.data)

    def test_save_file(self):
        from config_manager import YAMLConfigManager

        # Mock the open method and os methods
        m = mock_open()
        with patch("builtins.open", m), patch(
            "os.path.exists", return_value=False
        ), patch("os.makedirs"):
            manager = YAMLConfigManager(self.dummy_path)
            manager._data = self.data
            manager.save()

            written_data = "".join(call[0][0] for call in m().write.call_args_list)

            self.assertEqual(
                yaml.dump(self.data, default_flow_style=False), written_data
            )  # Use yaml.dump() with default_flow_style=False for readability
