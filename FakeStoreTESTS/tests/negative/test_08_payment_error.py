from os import wait
from pyexpat.errors import messages

from selenium.webdriver.common.by import By
from faker import Faker
from FakeStoreTESTS.data.userdata import DataToLogIn
from selenium.webdriver.support import expected_conditions as EC
from happy_path.base_test import BaseTest
import csv
import os


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

        # 5. enter a coupon code and click a button "Zastosuj kupon"
        # 6. use coupons from csv file
        file_path = os.path.join(os.path.dirname(__file__),'/home/student/PycharmProjects/PracaDyplomowaALK/FakeStoreTESTS/data/couponsTest.csv')

        # 7. take a valid code for this category
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile) # tu jest zwykly reader csv - ktory bierze liste a nie slownik
            rows = list(reader)
            coupon_code =rows[7][0]

        print (f' W tym tescie wybieramy kod dla kategorii windsurfing " {coupon_code} "- test pozytywny')
        #8. wait to insert a code
        self.wait.until(
            EC.visibility_of_element_located((By.NAME,'coupon_code'))
        ).send_keys(coupon_code)
        #9. click apply a coupon
        self.wait.until(
            EC.element_to_be_clickable((By.NAME,'apply_coupon'))
        ).click()
        #10 - check displayed message
        message_element = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME,'woocommerce-message' ))
        )
        #11. Check an expected result:
        actual_msg = message_element.text

        self.assertIn('Kupon został pomyślnie użyty', actual_msg)

        #12. Click a button "przejdz do platnosci"
        self.wait.until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, 'checkout-button.button.alt.wc-forward'))).click()

         #13. Check expected result - redirecting to subpage .../zamowienie/
        self.wait.until(EC.url_contains('zamowienie'))
        current_url = self.driver.current_url

        assert current_url == "https://fakestore.testelka.pl/zamowienie/"

        pass

