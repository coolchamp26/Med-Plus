import sys
import os
import unittest
import tkinter as tk

# Ensure we can import from root
sys.path.append(os.getcwd())

from medplus.ui.base import MedPlusApp, BaseFrame
from medplus.ui.login_ui import LoginFrame
from medplus.ui.dashboard_ui import UserDashboardFrame, AdminDashboardFrame

class TestUIAssets(unittest.TestCase):
    def setUp(self):
        self.app = MedPlusApp()
        self.app.withdraw() # Hide window
    
    def tearDown(self):
        self.app.destroy()

    def test_login_frame_init(self):
        """Test if LoginFrame initializes and loads background"""
        try:
            frame = LoginFrame(self.app)
            self.assertIsNotNone(frame.canvas, "Canvas should be created for background")
            # Check if image loaded (if file exists)
            # image0.png should exist in root
            if os.path.exists("image0.png"):
                self.assertIsNotNone(frame.original_image, "Image0 should be loaded")
            else:
                print("WARNING: image0.png not found in current directory")
        except Exception as e:
            self.fail(f"LoginFrame init failed: {e}")

    def test_dashboard_frame_init(self):
        """Test if UserDashboardFrame initializes and loads background"""
        try:
            frame = UserDashboardFrame(self.app, "testuser")
            self.assertIsNotNone(frame.canvas, "Canvas should be created for background")
            if os.path.exists("pills.png"):
                self.assertIsNotNone(frame.original_image, "pills.png should be loaded")
            else:
                print("WARNING: pills.png not found")
        except Exception as e:
            self.fail(f"UserDashboardFrame init failed: {e}")

if __name__ == '__main__':
    unittest.main()
