import csv
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from tests.Selenium_tests.happy_path.base_test import BaseTest


class BuyingHP(BaseTest):

    PRODUCTS = [
        "386",
        "393",
        "391",
        "4116",
        "389"
    ]

    SHOP_MENU = (
        By.ID,
        "menu-item-198"
    )

    CATEGORY = (
        By.CSS_SELECTOR,
        "#main ul li:first-child a"
    )

    CART_BUTTON = (
        By.CSS_SELECTOR,
        ".added_to_cart.wc-forward"
    )

    COUPON_FIELD = (
        By.NAME,
        "coupon_code"
    )

    APPLY_COUPON = (
        By.NAME,
        "apply_coupon"
    )

    ERROR_BOX = (
        By.ID,
        "coupon-error-notice"
    )

    def setUp(self):
        super().setUp()

        self.data_path = os.path.join(
            os.path.dirname(__file__),
            "../../../data/couponsTest.csv"
        )

    def test_buy_coupon_payment(self):

        #1. open shop
        self.wait.until(
            EC.element_to_be_clickable(
                self.SHOP_MENU
            )
        ).click()

        #2. choose category
        self.wait.until(
            EC.element_to_be_clickable(
                self.CATEGORY
            )
        ).click()

        #3. add products
        for product_id in self.PRODUCTS:

            self.home_page.close_banner()

            locator = (
                By.CSS_SELECTOR,
                f'[data-product_id="{product_id}"]'
            )

            element = self.wait.until(
                EC.element_to_be_clickable(locator)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);",
                element
            )

            try:
                element.click()
            except:
                self.driver.execute_script(
                    "arguments[0].click();",
                    element
                )

        #4. go to cart
        self.wait.until(
            EC.element_to_be_clickable(
                self.CART_BUTTON
            )
        ).click()

        #5. read expired coupon
        with open(self.data_path, newline="") as csvfile:
            rows = list(csv.reader(csvfile))
            coupon_code = rows[8][0]

        print(
            f'Kupon test (wygasły): {coupon_code}'
        )

        #6. apply coupon
        self.wait.until(
            EC.visibility_of_element_located(
                self.COUPON_FIELD
            )
        ).send_keys(coupon_code)

        self.wait.until(
            EC.element_to_be_clickable(
                self.APPLY_COUPON
            )
        ).click()

        #7. check error
        error = self.wait.until(
            EC.visibility_of_element_located(
                self.ERROR_BOX
            )
        )

        self.assertIn(
            "stracił",
            error.text.lower()
        )