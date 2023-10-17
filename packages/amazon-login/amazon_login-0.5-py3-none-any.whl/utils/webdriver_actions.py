from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebDriverActions:
    def __init__(self, chrome_driver, wait_time=5):
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

    def get_element(self, by_criterion, criterion_value, index=0):
        elements = self.wait.until(
            EC.presence_of_all_elements_located((by_criterion, criterion_value))
        )
        return elements[index]

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

    # def click_element_inside_shadow_root(
    #     self, host_criterion, host_value, internal_selector=None, open_first=False
    # ):
    #     """
    #     Clicks on an element inside a shadow root or the host element itself.

    #     :param host_criterion: The criterion to locate the host element.
    #     :param host_value: The value for the criterion to locate the host element.
    #     :param internal_selector: The CSS selector to find the element inside the shadow root.
    #                             If None, the host element is clicked.
    #     :param open_first: If True, clicks on the host element before clicking on the internal element.
    #     """
    #     host_element = self.wait.until(
    #         EC.presence_of_element_located((host_criterion, host_value))
    #     )

    #     if open_first:
    #         host_element.click()

    #     if internal_selector:
    #         # JavaScript to pierce through the shadow boundary and find the desired element
    #         js_script = """
    #         let hostElement = arguments[0];
    #         let shadowRoot = hostElement.shadowRoot;
    #         return shadowRoot.querySelector(arguments[1]);
    #         """

    #         # Execute the JavaScript and get the element inside the shadow root
    #         internal_element = self.driver.execute_script(
    #             js_script, host_element, internal_selector
    #         )

    #         # Click on the retrieved element
    #         internal_element.click()

    def interact_with_element_inside_shadow_root(
        self,
        host_criterion,
        host_value,
        *selectors,
        action="click",
        text=None,
        open_first=False,
        clear_first=False
    ):
        """
        Interacts with an element inside one or more nested shadow roots.

        :param host_criterion: The criterion to locate the host element.
        :param host_value: The value for the criterion to locate the host element.
        :param selectors: A list of CSS selectors to navigate through the shadow roots.
                        The last selector targets the element to be interacted with.
        :param action: The type of interaction - 'click' or 'send_keys'.
        :param text: The text to send if action is 'send_keys'.
        :param open_first: If True, clicks on the host element before navigating the shadow roots.
        :param clear_first: If True, clears the content of the input field before sending keys.
        """
        host_element = self.wait.until(
            EC.presence_of_element_located((host_criterion, host_value))
        )

        if open_first:
            host_element.click()

        element = host_element

        # Traverse through the shadow roots using the provided selectors
        for selector in selectors:
            js_script = """
            let element = arguments[0];
            let shadowRoot = element.shadowRoot;
            return shadowRoot.querySelector(arguments[1]);
            """
            element = self.driver.execute_script(js_script, element, selector)

        # Perform the specified action on the final retrieved element
        if action == "click":
            element.click()
        elif action == "send_keys":
            if clear_first:
                element.clear()
            if text is not None:
                element.send_keys(text)
