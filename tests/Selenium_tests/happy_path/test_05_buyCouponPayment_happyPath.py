from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from tests.Selenium_tests.happy_path.base_test import BaseTest

from pages.home_page import HomePage

from data.userdata import UserData

import csv
import random
import os


class BuyingHP(BaseTest):

    VALID_COUPON_ROW = 7

    PRODUCTS = [
        "386",
        "393",
        "391",
        "4116",
        "389"
    ]

    def setUp(self):

        super().setUp()

        self.home_page = HomePage(
            self.driver
        )

        self.BASE_DIR = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(__file__)
                )
            )
        )

        self.DATA_PATH = os.path.join(
            self.BASE_DIR,
            "data"
        )

    def add_products_to_cart(self):

        #1.primary menu on main page - click Sklep
        self.home_page.open_shop()

        #2.choose category windsurfing
        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "#main ul li:first-child a"
                )
            )
        ).click()

        self.home_page.hide_banner()

        #3.add products to cart
        for product_id in self.PRODUCTS:

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

            element.click()

        #4.go to cart
        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    ".added_to_cart"
                )
            )
        ).click()

    def apply_coupon(self):

        file_path = os.path.join(
            self.DATA_PATH,
            "couponsTest.csv"
        )

        with open(file_path) as csvfile:

            rows = list(
                csv.reader(
                    csvfile
                )
            )

        coupon = rows[
            self.VALID_COUPON_ROW
        ][0]

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

        self.driver.find_element(
            By.NAME,
            "apply_coupon"
        ).click()

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

    def go_to_payment(self):

        self.home_page.hide_banner()

        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.CLASS_NAME,
                    "checkout-button"
                )
            )
        ).click()

        self.wait.until(
            EC.url_contains(
                "zamowienie"
            )
        )

        self.assertIn(
            "zamowienie",
            self.driver.current_url
        )

    def fill_user_data(self):

        fields = {

            "billing_email":
                UserData.DATA_EMAIL,

            "billing_first_name":
                UserData.DATA_FIRST_NAME,

            "billing_last_name":
                UserData.DATA_LAST_NAME,

            "billing_address_1":
                UserData.DATA_STREET,

            "billing_postcode":
                UserData.DATA_POSTAL_CODE,

            "billing_city":
                UserData.DATA_CITY,

            "billing_phone":
                UserData.DATA_PHONE
        }

        for field, value in fields.items():

            self.driver.find_element(
                By.ID,
                field
            ).send_keys(
                value
            )

    def make_payment(self):

        pass

    def check_order(self):

        self.assertIn(
            "zamowienie",
            self.driver.current_url
        )

    def test_buy_coupon_payment(self):

        self.add_products_to_cart()

        self.apply_coupon()

        self.go_to_payment()

        self.fill_user_data()