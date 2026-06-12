from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage


class HomePage(BasePage):

    ACCOUNT_MENU = (
        By.ID,
        "menu-item-201"
    )

    SHOP_MENU = (
        By.ID,
        "menu-item-198"
    )

    STORE_NOTICE = (
        By.CLASS_NAME,
        "woocommerce-store-notice"
    )

    CLOSE_NOTICE = (
        By.CLASS_NAME,
        "woocommerce-store-notice__dismiss-link"
    )

    LOGO = (
        By.CLASS_NAME,
        "custom-logo"
    )

    CLIMBING_CATEGORY = (
        By.PARTIAL_LINK_TEXT,
        "Wspinaczka"
    )

    REGISTRATION_EMAIL = (
        By.ID,
        "reg_email"
    )

    def close_banner(self):

        try:

            button = self.wait.until(
                EC.element_to_be_clickable(
                    self.CLOSE_NOTICE
                )
            )

            button.click()

            self.wait.until(
                EC.invisibility_of_element_located(
                    self.STORE_NOTICE
                )
            )

        except TimeoutException:

            pass

    def open_my_account(self):

        self.close_banner()

        self.click(
            self.ACCOUNT_MENU
        )

    def open_shop(self):

        self.close_banner()

        self.click(
            self.SHOP_MENU
        )

    def go_home(self):

        self.click(
            self.LOGO
        )

    def open_climbing_category(self):

        self.click(
            self.CLIMBING_CATEGORY
        )

    def is_my_account_opened(self):

        return (
            "moje-konto"
            in
            self.get_current_url()
        )