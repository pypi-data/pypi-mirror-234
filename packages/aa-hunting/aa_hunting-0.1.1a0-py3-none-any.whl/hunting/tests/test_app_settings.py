from unittest.mock import patch

from django.test import TestCase

from ..app_settings import (
    HUNTING_ENABLE_CORPTOOLS_IMPORT, HUNTING_TASK_PRIORITY, corptools_active,
    discordbot_active, killtracker_active,
)


class TestFunctions(TestCase):
    @patch('django.apps.apps.is_installed')
    def test_discordbot_active(self, mock_is_installed):
        # Test that discordbot_active returns True when the app is installed
        mock_is_installed.return_value = True
        self.assertTrue(discordbot_active())

        # Test that discordbot_active returns False when the app is not installed
        mock_is_installed.return_value = False
        self.assertFalse(discordbot_active())

    @patch('django.apps.apps.is_installed')
    def test_corptools_active(self, mock_is_installed):
        # Test that corptools_active returns True when the app is installed
        mock_is_installed.return_value = True
        self.assertTrue(corptools_active())

        # Test that corptools_active returns False when the app is not installed
        mock_is_installed.return_value = False
        self.assertFalse(corptools_active())

    @patch('django.apps.apps.is_installed')
    def test_killtracker_active(self, mock_is_installed):
        # Test that killtracker_active returns True when the app is installed
        mock_is_installed.return_value = True
        self.assertTrue(killtracker_active())

        # Test that killtracker_active returns False when the app is not installed
        mock_is_installed.return_value = False
        self.assertFalse(killtracker_active())

    def test_HUNTING_TASK_PRIORITY(self):
        # Test that HUNTING_TASK_PRIORITY is defined and is a string
        self.assertIsInstance(HUNTING_TASK_PRIORITY, str)

    def test_HUNTING_ENABLE_CORPTOOLS_IMPORT(self):
        # Test that HUNTING_ENABLE_CORPTOOLS_IMPORT is defined and is a boolean
        self.assertIsInstance(HUNTING_ENABLE_CORPTOOLS_IMPORT, bool)
