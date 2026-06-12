import csv
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from tests.Selenium_tests.happy_path.base_test import BaseTest
from data.userdata import UserData


class BuyingHP(BaseTest):

    PRODUCTS = ["386", "393", "391", "4116", "389"]

    SHOP_MENU = (By.ID, "menu-item-198")

    CATEGORY = (By.XPATH, '//*[@id="main"]/ul/li[1]//a')

    CART_BUTTON = (By.CSS_SELECTOR, ".added_to_cart.wc-forward")

    CHECKOUT_BUTTON = (By.CSS_SELECTOR, ".checkout-button.button.alt.wc-forward")

    TERMS = (By.ID, "terms")

    PLACE_ORDER = (By.ID, "place_order")

    def setUp(self):
        super().setUp()

        self.coupon_path = os.path.join(
            os.path.dirname(__file__),
            "../../../data/couponsTest.csv"
        )

        self.cards_path = os.path.join(
            os.path.dirname(__file__),
            "../../../data/credit_cards.csv"
        )

    def test_payment_error(self):

        #1. open shop
        self.home_page.close_banner()

        self.wait.until(
            EC.element_to_be_clickable(
                self.SHOP_MENU
            )
        ).click()

        #2. category
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

            self.home_page.scroll_to(element)

            try:
                element.click()
            except:
                self.driver.execute_script(
                    "arguments[0].click();",
                    element
                )

        #4. cart
        self.home_page.close_banner()

        self.wait.until(
            EC.element_to_be_clickable(
                self.CART_BUTTON
            )
        ).click()

        #5. coupon
        with open(self.coupon_path, newline="") as csvfile:
            rows = list(csv.reader(csvfile))
            coupon_code = rows[7][0]

        self.wait.until(
            EC.visibility_of_element_located(
                (By.NAME, "coupon_code")
            )
        ).send_keys(coupon_code)

        self.wait.until(
            EC.element_to_be_clickable(
                (By.NAME, "apply_coupon")
            )
        ).click()

        message = self.wait.until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "woocommerce-message")
            )
        )

        self.assertIn(
            "Kupon został pomyślnie użyty",
            message.text
        )

        #6. checkout
        self.home_page.close_banner()

        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )

        self.wait.until(
            EC.element_to_be_clickable(
                self.CHECKOUT_BUTTON
            )
        ).click()

        self.wait.until(
            EC.url_contains("zamowienie")
        )

        self.assertEqual(
            self.driver.current_url,
            "https://fakestore.testelka.pl/zamowienie/"
        )

        #7. billing data
        self.wait.until(
            EC.visibility_of_element_located((By.ID, "billing_email"))
        ).send_keys(UserData.DATA_EMAIL)

        self.driver.find_element(By.ID, "billing_first_name").send_keys(UserData.DATA_FIRST_NAME)
        self.driver.find_element(By.ID, "billing_last_name").send_keys(UserData.DATA_LAST_NAME)
        self.driver.find_element(By.ID, "billing_address_1").send_keys(UserData.DATA_STREET)
        self.driver.find_element(By.ID, "billing_postcode").send_keys(UserData.DATA_POSTAL_CODE)
        self.driver.find_element(By.ID, "billing_city").send_keys(UserData.DATA_CITY)
        self.driver.find_element(By.ID, "billing_phone").send_keys(UserData.DATA_PHONE)

        #8. card
        with open(self.cards_path, newline="") as csvfile:
            reader = list(csv.DictReader(csvfile))
            row = reader[5]

            number = row["number"]
            expiry_date = row["expiry_date"]
            cvv = row["cvv"]

        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.CSS_SELECTOR, "iframe[name^='__privateStripeFrame']")
            )
        )

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "payment-numberInput"))
        ).send_keys(number)

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "payment-expiryInput"))
        ).send_keys(expiry_date)

        self.wait.until(
            EC.visibility_of_element_located((By.ID, "payment-cvcInput"))
        ).send_keys(cvv)

        self.driver.switch_to.default_content()

        #9. terms
        self.home_page.close_banner()

        checkbox = self.wait.until(
            EC.element_to_be_clickable(self.TERMS)
        )

        if not checkbox.is_selected():
            try:
                checkbox.click()
            except:
                self.driver.execute_script(
                    "arguments[0].click();",
                    checkbox
                )

        #10. order
        self.home_page.close_banner()

        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )

        self.wait.until(
            EC.element_to_be_clickable(self.PLACE_ORDER)
        ).click()

        #11. error validation
        error_element = self.wait.until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "woocommerce-error")
            )
        )

        self.assertTrue(
            "przeszłości" in error_element.text
            or "expiry" in error_element.text.lower()
        )