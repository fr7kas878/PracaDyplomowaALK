from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.home_page import HomePage


class MyAccountPage(BasePage):

    EMAIL = (
        By.ID,
        "reg_email"
    )

    PASSWORD = (
        By.ID,
        "reg_password"
    )

    SHOW_PASSWORD = (
        By.CSS_SELECTOR,
        '[aria-label="Pokaż hasło"]'
    )

    REGISTER = (
        By.CLASS_NAME,
        "woocommerce-form-register__submit"
    )

    DELETE_ACCOUNT = (
        By.CLASS_NAME,
        "delete-me"
    )

    def register_new_user(
            self,
            email,
            password
    ):

        HomePage(
            self.driver
        ).close_banner()

        self.type(
            self.EMAIL,
            email
        )

        self.type(
            self.PASSWORD,
            password
        )

        HomePage(
            self.driver
        ).close_banner()

        self.click(
            self.SHOW_PASSWORD
        )

        self.click(
            self.REGISTER
        )

    def registration_successful(self):

        return self.is_visible(
            self.DELETE_ACCOUNT
        )