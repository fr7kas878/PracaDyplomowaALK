from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from FakeStoreTESTS.Selenium_tests.happy_path.base_test import BaseTest
import csv
import random
import os


class BuyingCouponsOnly(BaseTest):

    def setUp(self):
        super().setUp()

        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.DATA_PATH = os.path.join(self.BASE_DIR, 'data')

    def add_products_to_cart(self):
        # 1. primary menu on main page - click Sklep
        self.driver.find_element(By.XPATH, '//*[@id="menu-item-198"]').click()
        # 2. choose a first category - windsurfing[1]
        element = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/ul/li[1]//a')))
        element.click()

        # 3. add to cart several products -->adding several products in a loop by product_id :

        products = ["386", "393", "391", "4116", "389"]
        for product_id in products:
            self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-product_id="{product_id}"]'))).click()

        # 4.click button "Zobacz koszyk" to go to cart
        self.wait.until(
            EC.element_to_be_clickable
            ((By.CSS_SELECTOR, '.added_to_cart.wc-forward'))).click()

    def apply_multiple_coupons(self):
        # 5. enter a coupon code and click a button "Zastosuj kupon"
        # 6. use coupons from csv file
        file_path = os.path.join(self.DATA_PATH, 'couponsTest.csv')

        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = [row for row in reader if row and row[0].strip() != ""]

        # 7. randomly select 5 coupons WITHOUT repetition
        coupons = random.sample(rows, min(5, len(rows)))

        for coupon_row in coupons:
            coupon_code = coupon_row[0].strip()

            print(f' W tym tescie wylosowano kod " {coupon_code} "')

            # 8. wait until coupon input is ready (after DOM refresh)
            field = self.wait.until(
                EC.element_to_be_clickable((By.NAME, 'coupon_code'))
            )
            field.clear()
            field.send_keys(coupon_code)

            # 9. click apply a coupon
            self.wait.until(
                EC.element_to_be_clickable((By.NAME, 'apply_coupon'))
            ).click()

            # wait until coupon is processed (DOM refresh safety)
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, 'woocommerce-message'))
            )

            # 10 - check displayed message
            message_element = self.wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'woocommerce-message'))
            )

            # 11. Check an expected result:
            actual_msg = message_element.text
            self.assertTrue('Kupon' in actual_msg)

    def get_cart_total(self):
        # 12. helper to read total price from cart
        total_element = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.order-total .amount'))
        )
        total_text = total_element.text

        # 13. remove currency + spaces (important for WooCommerce format)
        cleaned = (
            total_text
            .replace('zł', '')
            .replace('\xa0', '')  # hard space
            .replace(' ', '')  # normal space
            .replace(',', '.')
            .strip()
        )
        price = float(cleaned)
        return price

    # @unittest.skip("Temporary skipping")
    def test_multiple_coupons_price_reduction(self):
        self.add_products_to_cart()

        # 14. initial price before coupons
        initial_total = self.get_cart_total()
        print(f'Suma twojego zamowienia przed znizkami: {initial_total}')

        self.apply_multiple_coupons()

        # 15. final price after coupons
        final_total = self.get_cart_total()
        print(f'Suma twojego zamowienia po znizkach: {final_total}')

        # 16. Check expected result: price is reduced
        self.assertLess(final_total, initial_total)

        # calculate difference
        reduction = initial_total - final_total
        print(f'Zaoszczedziles dzieki kuponom : {reduction} zlotych!')