from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class BasePage:

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(
            driver,
            10
        )

    def click(self, locator):

        self.wait.until(
            EC.element_to_be_clickable(locator)
        ).click()

    def type(self, locator, value):

        field = self.wait.until(
            EC.visibility_of_element_located(locator)
        )

        field.clear()

        field.send_keys(value)

    def is_visible(self, locator):

        return self.wait.until(
            EC.visibility_of_element_located(locator)
        ).is_displayed()

    def get_text(self, locator):

        return self.wait.until(
            EC.visibility_of_element_located(locator)
        ).text

    def get_validation_message(self, locator):

        field = self.wait.until(
            EC.visibility_of_element_located(locator)
        )

        return self.driver.execute_script(
            "return arguments[0].validationMessage;",
            field
        )

    def get_current_url(self):

        return self.driver.current_url

    def scroll_to(self, element):

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            element
        )


    def hide_banner(self):

        try:
            banner = self.driver.find_element(By.CLASS_NAME, "demo_store")
            self.driver.execute_script(
                "arguments[0].remove();",
                banner
            )
        except NoSuchElementException:
            pass
