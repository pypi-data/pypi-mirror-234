# from vendor_central.vendor_login import VendorLogin
from utils.webdriver_actions import WebDriverActions
from utils.driver import ChromeDriver
from amazon_services.login import Login


class AmazonManager:
    def __init__(
        self,
        username,
        password,
        login_link,
        amazon_xpaths,
        sender_email,
        recipient_emails,
        type,
        chrome_driver=None,
        download_path=None,
    ):
        if chrome_driver is None:
            chrome_driver = ChromeDriver(type, download_path)
        self.driver_actions = WebDriverActions(chrome_driver)
        self.login_module = Login(
            self.driver_actions,
            username,
            password,
            login_link,
            amazon_xpaths,
            sender_email,
            recipient_emails,
            type,
        )

    def login(self):
        return self.login_module.login()
