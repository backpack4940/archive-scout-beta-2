from __future__ import annotations

import unittest

from archive_scout.ui import main_window
from archive_scout.ui.event_queue import CoalescingEventQueue


class Beta21StartupTests(unittest.TestCase):
    def test_main_window_imports_bounded_event_queue(self):
        self.assertIs(main_window.CoalescingEventQueue, CoalescingEventQueue)

    def test_public_version_is_beta_2_1(self):
        self.assertEqual(main_window.VERSION, "3.0.0-beta.2.1")


if __name__ == "__main__":
    unittest.main()
