import csv
import os
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

from pages.home_page import HomePage

from tests.Selenium_tests.happy_path.base_test import BaseTest


class BuyingHP(BaseTest):

    PRODUCTS = [
        "386",
        "393",
        "391",
        "4116",
        "389"
    ]

    CATEGORY = (
        By.CSS_SELECTOR,
        "#main ul li:first-child a"
    )

    CART = (
        By.CSS_SELECTOR,
        ".added_to_cart.wc-forward"
    )

    def setUp(self):

        super().setUp()

        self.home_page = HomePage(
            self.driver
        )

        self.data_path = os.path.join(
            os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    "../../../data/couponsTest.csv"
                )
            )
        )

    def add_products(self):

        #1.primary menu on main page - click Sklep
        self.home_page.open_shop()

        #2.choose category - windsurfing
        self.wait.until(
            EC.element_to_be_clickable(
                self.CATEGORY
            )
        ).click()

        for product_id in self.PRODUCTS:

            self.home_page.hide_banner()

            locator = (
                By.CSS_SELECTOR,
                f'[data-product_id="{product_id}"]'
            )

            element = self.wait.until(
                EC.element_to_be_clickable(
                    locator
                )
            )

            self.home_page.scroll_to(
                element
            )

            try:

                element.click()

            except ElementClickInterceptedException:

                self.driver.execute_script(
                    "arguments[0].click();",
                    element
                )

            self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        ".added_to_cart"
                    )
                )
            )

    def open_cart(self):

        self.home_page.hide_banner()

        self.wait.until(
            EC.element_to_be_clickable(
                self.CART
            )
        ).click()

    def get_random_coupon(self):

        with open(
                self.data_path,
                newline=""
        ) as csvfile:

            coupons = [

                row["code"]

                for row in csv.DictReader(
                    csvfile
                )

                if row.get(
                    "code"
                )
            ]

        coupon = random.choice(
            coupons
        )

        print(
            f'Wylosowany kupon: {coupon}'
        )

        return coupon

    def apply_coupon(
            self,
            coupon
    ):

        self.home_page.hide_banner()

        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.NAME,
                    "coupon_code"
                )
            )
        ).send_keys(
            coupon
        )

        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.NAME,
                    "apply_coupon"
                )
            )
        ).click()

    def test_buy_coupon_payment(self):

        self.add_products()

        self.open_cart()

        coupon = self.get_random_coupon()

        self.apply_coupon(
            coupon
        )

        #check expected result
        message = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.CLASS_NAME,
                    "woocommerce-message"
                )
            )
        )

        self.assertIn(
            "Kupon został pomyślnie użyty",
            message.text
        )