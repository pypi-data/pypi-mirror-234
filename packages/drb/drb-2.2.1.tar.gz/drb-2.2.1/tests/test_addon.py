import unittest
from drb.addons.addon import AddonManager


class TestAddonManager(unittest.TestCase):
    manager: AddonManager = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.manager = AddonManager()

    def test_get_all_addons(self):
        addons = self.manager.get_all_addons()
        self.assertEqual(2, len(addons))

    def test_get_addon(self):
        addon = self.manager.get_addon('geolocation')
        self.assertEqual('geolocation', addon.identifier())
        self.assertEqual(dict, addon.return_type())
