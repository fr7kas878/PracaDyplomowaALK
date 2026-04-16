from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from FakeStoreTESTS.Selenium_tests.happy_path.base_test import BaseTest
import csv


class BuyingHP(BaseTest):

    def setUp(self):
        super().setUp()

    # @unittest.skip("Temporary skipping")
    def test_buy_coupon_payment(self):
        # 1. primary menu on main page - click Sklep
        self.driver.find_element(By.XPATH, '//*[@id="menu-item-198"]').click()
        # 2. choose a first category - windsurfing[1]
        element = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/ul/li[1]//a'))
        )
        element.click()

        # 3. add to cart several products
        #adding several products in a loop by product_id :

        products = ["386", "393", "391", "4116", "389"]
        for product_id in products:
            self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-product_id="{product_id}"]'))
            ).click()

        # 4.click button "Zobacz koszyk" to go to cart
        self.wait.until(
            EC.element_to_be_clickable
            ((By.CSS_SELECTOR, '.added_to_cart.wc-forward'))
        ).click()

        # 5. enter a coupon code and click a button "Zastosuj kupoon"
        # 6. coupons from csv file
        file_path = '/FakeStoreTESTS/data/couponsTest.csv'

        # 7. take a random code
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)  # tu jest zwykly reader csv - ktory bierze liste, a nie slownik
            rows = list(reader)
            coupon_code = rows[8][0]

        print(f' W tym tescie wybieramy kod, ktory stracil waznosc: " {coupon_code} "- test negatywny')

        #8. insert a coupon code
        self.wait.until(
            EC.visibility_of_element_located((By.NAME,'coupon_code'))
        ).send_keys(coupon_code)

        #9. click aplly coupon
        self.wait.until(
            EC.element_to_be_clickable((By.NAME,'apply_coupon'))
        ).click()

        #10. check if the code is still valid
        self.wait.until(
            EC.visibility_of_element_located((By.ID,'coupon-error-notice' ))
        )
        # 11. check an expected result - message  " Kupon stracil waznosc"
        error = self.wait.until(
            EC.visibility_of_element_located((By.ID, 'coupon-error-notice'))
        )

        self.assertIn("stracił ważność", error.text.lower())
