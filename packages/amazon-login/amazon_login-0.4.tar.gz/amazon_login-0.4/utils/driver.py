import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime


class ChromeDriver:
    def __init__(self, type, download_path=None):
        # Set download path
        if not download_path:
            current_date_time = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
            self.download_path = os.path.join(os.getcwd(), "tmp", current_date_time)
        else:
            self.download_path = download_path

        # Set chrome profile path
        self.chrome_profile_path = os.path.join(os.getcwd(), f"chrome_profile_{type}")

        # Initialize the driver
        self.driver = self.init_driver()

    def init_driver(self):
        options = Options()

        # Create a new Chrome profile if the specified directory does not exist
        if not os.path.exists(self.chrome_profile_path):
            os.makedirs(self.chrome_profile_path)
            options.add_argument(
                "--no-first-run"
            )  # Skip the first-run dialog for new profiles

        options.add_argument(f"user-data-dir={self.chrome_profile_path}")
        options.add_argument(
            "profile-directory=Default"
        )  # Use the same profile directory

        # Create download directory if it doesn't exist
        os.makedirs(self.download_path, exist_ok=True)

        # Add download directory to Chrome preferences
        prefs = {"download.default_directory": self.download_path}
        options.add_experimental_option("prefs", prefs)

        # Instantiate the Chrome driver
        driver = webdriver.Chrome(options=options)

        return driver
