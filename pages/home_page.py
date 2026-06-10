from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage


class HomePage(BasePage):

    ACCOUNT_MENU = (
        By.ID,
        "menu-item-201"
    )

    STORE_NOTICE = (
        By.CLASS_NAME,
        "woocommerce-store-notice"
    )

    CLOSE_NOTICE = (
        By.CLASS_NAME,
        "woocommerce-store-notice__dismiss-link"
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