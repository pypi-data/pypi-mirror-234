from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebDriverActions:
    def __init__(self, chrome_driver, wait_time=10):
        self.driver = chrome_driver.driver
        self.download_path = chrome_driver.download_path
        self.wait = WebDriverWait(self.driver, wait_time)

    def enter_text(self, by_criterion, criterion_value, text):
        element = self.wait.until(
            EC.presence_of_element_located((by_criterion, criterion_value))
        )
        element.clear()
        element.send_keys(text)

    def click_element(self, by_criterion, criterion_value, index=0):
        elements = self.wait.until(
            EC.presence_of_all_elements_located((by_criterion, criterion_value))
        )
        elements[index].click()

    def get_session_cookies(self):
        """Fetch session cookies."""
        cookies = self.driver.get_cookies()
        session_cookies = {cookie["name"]: cookie["value"] for cookie in cookies}
        return session_cookies

    def get_csrf_token(
        self,
        csrf_link,
        by_criterion,
        csrf_token_name,
    ):
        """Fetch CSRF token."""
        self.driver.get(csrf_link)
        csrf_token_element = self.wait.until(
            EC.presence_of_element_located((by_criterion, csrf_token_name))
        )
        return csrf_token_element.get_attribute("value")

    def get(self, url):
        """Navigate to a URL."""
        self.driver.get(url)

    def quit(self):
        """Quit the browser."""
        self.driver.quit()

    @property
    def current_url(self):
        """Get the current URL."""
        return self.driver.current_url

    def is_element_present(self, by_criterion, criterion_value):
        elements = self.driver.find_elements(by_criterion, criterion_value)
        return len(elements) > 0
