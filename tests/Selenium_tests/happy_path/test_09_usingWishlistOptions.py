from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.home_page import HomePage

from tests.Selenium_tests.happy_path.test_03_login_myaccount_happyPath import (
    LogToMyAccount
)


class UsingWishlistOptions(LogToMyAccount):

    PRODUCT = (
        By.XPATH,
        '//a[contains(@href,"gran-koscielcow")]'
    )

    ADD_TO_WISHLIST = (
        By.XPATH,
        '//a[contains(@class,"add_to_wishlist")]'
    )

    OPEN_WISHLIST = (
        By.XPATH,
        '//a[contains(@href,"wishlist")]'
    )

    PRODUCT_IN_WISHLIST = (
        By.XPATH,
        '//a[contains(@href,"gran-koscielcow")]'
    )

    def setUp(self):

        super().setUp()

        self.home_page = HomePage(
            self.driver
        )

    def test_addingToWishlist(self):

        # login reused from base class (LogToMyAccount)
        self.login()

        #1.Go to mainpage and choose category "wspinaczka"
        self.home_page.go_home()

        self.home_page.open_climbing_category()

        #2.click to product
        self.wait.until(
            EC.element_to_be_clickable(
                self.PRODUCT
            )
        ).click()

        #2a.click add to wishlist if not exists
        try:

            self.wait.until(
                EC.element_to_be_clickable(
                    self.ADD_TO_WISHLIST
                )
            ).click()

        except TimeoutException:

            pass

        #3.open wishlist
        self.wait.until(
            EC.element_to_be_clickable(
                self.OPEN_WISHLIST
            )
        ).click()

        #4.check expected result
        product = self.wait.until(
            EC.visibility_of_element_located(
                self.PRODUCT_IN_WISHLIST
            )
        )

        self.assertTrue(
            product.is_displayed(),
            "Product not in wishlist"
        )