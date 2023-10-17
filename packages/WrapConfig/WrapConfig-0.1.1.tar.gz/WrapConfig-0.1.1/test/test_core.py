import unittest
from unittest.mock import patch, mock_open


class TestConfigManager(unittest.TestCase):
    def setUp(self):
        from config_manager import ConfigManager

        class MockConfigManager(ConfigManager):
            def load(self):
                pass  # No-op implementation

            def save(self):
                pass  # No-op implementation

        self.manager = MockConfigManager()

    def test_set_and_save(self):
        with patch.object(self.manager, "save") as mock_save:
            self.manager.set("key", value="value")
            self.assertEqual(self.manager._data["key"], "value")
            mock_save.assert_called_once()

    def test_set_with_subkeys(self):
        self.manager.set("key", "subkey1", "subkey2", value="value")
        self.assertEqual(self.manager._data["key"]["subkey1"]["subkey2"], "value")

    def test_set_without_autosave(self):
        with patch.object(self.manager, "save") as mock_save:
            self.manager = self.manager.__class__(default_save=False)
            self.manager.set("key", value="value")
            mock_save.assert_not_called()

    def test_set_with_save_override(self):
        with patch.object(self.manager, "save") as mock_save:
            self.manager.set("key", value="value", save=False)
            mock_save.assert_not_called()

    def test_set_error_handling(self):
        self.manager._data["key"] = "value"
        with self.assertRaises(TypeError):
            self.manager.set("key", "subkey", value="value2")

    def test_get_key(self):
        self.manager._data["key"] = "value"
        result = self.manager.get("key")
        self.assertEqual(result, "value")

    def test_get_subkeys(self):
        self.manager._data["key"] = {"subkey1": {"subkey2": "value"}}
        result = self.manager.get("key", "subkey1", "subkey2")
        self.assertEqual(result, "value")

    def test_get_default(self):
        result = self.manager.get("non_existent_key", default="default_val")
        self.assertEqual(result, "default_val")

    def test_get_error_handling(self):
        self.manager._data["key"] = "value"
        with self.assertRaises(TypeError):
            self.manager.get("key", "subkey")

    def test_update(self):
        initial_data = {"key1": "value1", "key2": {"subkey1": "value2"}}
        update_data = {"key2": {"subkey2": "value3"}, "key3": "value4"}
        self.manager._data = initial_data
        self.manager.update(update_data)

        expected_data = {
            "key1": "value1",
            "key2": {"subkey1": "value2", "subkey2": "value3"},
            "key3": "value4",
        }
        self.assertEqual(self.manager._data, expected_data)

    def test_fill(self):
        initial_data = {"key1": "value1", "key2": {"subkey1": "value2"}}
        fill_data = {"key1": "value2", "key2": {"subkey2": "value3"}, "key3": "value4"}
        self.manager._data = initial_data
        self.manager.fill(fill_data)

        expected_data = {
            "key1": "value1",
            "key2": {"subkey1": "value2", "subkey2": "value3"},
            "key3": "value4",
        }
        self.assertEqual(self.manager._data, expected_data)

    def test_data_property(self):
        initial_data = {"key": "value"}
        self.manager._data = initial_data
        data_copy = self.manager.data
        data_copy["key"] = "modified"

        self.assertEqual(self.manager._data["key"], "value")
        self.assertNotEqual(data_copy["key"], self.manager._data["key"])
