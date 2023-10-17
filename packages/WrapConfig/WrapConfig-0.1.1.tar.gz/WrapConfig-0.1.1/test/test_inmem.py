import unittest


class TestInMemoryConfig(unittest.TestCase):
    def setUp(self):
        from config_manager import InMemoryConfig

        self.manager = InMemoryConfig()

    def test_initial_data(self):
        """Test that initial data is an empty dictionary."""
        self.assertEqual(self.manager._data, {})

    def test_save(self):
        """Test that the save method backs up data correctly."""
        self.manager._data = {"key": "value"}
        self.manager.save()
        self.assertEqual(self.manager._backup, {"key": "value"})

    def test_load_without_previous_save(self):
        """Test that loading without a previous save results in empty data."""
        self.manager.load()
        self.assertEqual(self.manager._data, {})

    def test_load_with_previous_save(self):
        """Test that loading restores data from backup."""
        self.manager._data = {"key": "value"}
        self.manager.save()
        self.manager._data = {}
        self.manager.load()
        self.assertEqual(self.manager._data, {"key": "value"})

    def test_set_and_save(self):
        """Test that setting a value and then saving works correctly."""
        self.manager.set("key", value="value")
        self.manager.save()
        self.assertEqual(self.manager._backup, {"key": "value"})

    def test_load_after_set_and_save(self):
        """Test that loading after setting a value and saving restores data correctly."""
        self.manager.set("key", value="value")
        self.manager.save()
        self.manager._data = {}
        self.manager.load()
        self.assertEqual(self.manager._data, {"key": "value"})


if __name__ == "__main__":
    unittest.main()
