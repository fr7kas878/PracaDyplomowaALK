from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from FakeStoreTESTS.Selenium_tests.happy_path.base_test import BaseTest
from FakeStoreTESTS.data.userdata import UserData
import csv
import random
import os


class BuyingHP(BaseTest):

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

        #2a. hide blocking banner
        try:
            banner = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "demo_store"))
            )
            self.driver.execute_script("arguments[0].style.display='none';", banner)
        except:
            pass  # banner not always present

        # 3. add to cart several products -->adding several products in a loop by product_id :
        products = ["386", "393", "391", "4116", "389"]

        for product_id in products:
            element = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-product_id="{product_id}"]'))  )

            # 3a. scroll to element to avoid overlay errors
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

            # 3b. fix dummy errors by adding wait
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-product_id="{product_id}"]')))
            element.click()

        # 4.click button "Zobacz koszyk" to go to cart
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.added_to_cart.wc-forward')) ).click()

    def apply_coupon(self):
        # 5. enter a coupon code and click a button "Zastosuj kupon"
        # 6. use coupons from csv file
        file_path = os.path.join(self.DATA_PATH, 'couponsTest.csv')
        # 7. take a valid code for this category
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)  # tu jest zwykly reader csv - ktory bierze liste a nie slownik
            rows = list(reader)
            coupon_code = rows[7][0]

        print(f' W tym tescie wybieramy kod dla kategorii windsurfing " {coupon_code} "- test pozytywny')
        # 8. wait to insert a code
        self.wait.until(
            EC.visibility_of_element_located((By.NAME, 'coupon_code'))
        ).send_keys(coupon_code)
        # 9. click apply a coupon
        self.wait.until(
            EC.element_to_be_clickable((By.NAME, 'apply_coupon'))
        ).click()
        # 10 - check displayed message
        message_element = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'woocommerce-message'))
        )
        # 11. Check an expected result:
        actual_msg = message_element.text
        self.assertIn('Kupon został pomyślnie użyty', actual_msg)

    def go_to_payment(self):
        #first hide blocking banner again (page refresing cuser, it appears again)
        try:
            banner = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "demo_store"))
            )
            self.driver.execute_script("arguments[0].style.display='none';", banner)
        except:
            pass  # banner not always present

        # 12. Click a button "przejdz do platnosci"
        element = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.checkout-button.button.alt.wc-forward')) )

         #12a. scroll to avoid overlay errors
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

        element.click()

        # 13. Check expected result - redirecting to subpage .../zamowienie/
        self.wait.until(EC.url_contains('zamowienie'))
        current_url = self.driver.current_url
        self.assertEqual(current_url, "https://fakestore.testelka.pl/zamowienie/")
    def fill_user_data(self):
        # 14. Fulfill an order data
        # 14a. email - from email generator
        generated_email = UserData.DATA_EMAIL
        self.driver.find_element(By.ID, 'billing_email').send_keys(generated_email)
        # 14b. Name
        firstname = UserData.DATA_FIRST_NAME
        self.driver.find_element(By.ID, 'billing_first_name').send_keys(firstname)
        # 14c. Lastname
        lastname = UserData.DATA_LAST_NAME
        self.driver.find_element(By.ID, 'billing_last_name').send_keys(lastname)
        # 14d. Street
        street = UserData.DATA_STREET
        self.driver.find_element(By.ID, 'billing_address_1').send_keys(street)
        # 14.e Postal code
        postalcode = UserData.DATA_POSTAL_CODE
        self.driver.find_element(By.ID, 'billing_postcode').send_keys(postalcode)
        # 14.f City
        city = UserData.DATA_CITY
        self.driver.find_element(By.ID, 'billing_city').send_keys(city)
        # 14.g phone_number
        phone = UserData.DATA_PHONE
        self.driver.find_element(By.ID, 'billing_phone').send_keys(phone)

    def make_payment(self):
        # 15 FAKE CARD PAYMENT DATA

        file_path = os.path.join(self.DATA_PATH, 'credit_cards.csv')

        with open(file_path, newline='') as csvfile:
            reader = list(csv.DictReader(csvfile))
            row = random.choice(reader)

            number = row["number"]
            expiry_date = row["expiry_date"]
            cvv = row["cvv"]

            print(f' W tym tescie wylosowano karte kredytowa o parametrach: {number}, {expiry_date}, {cvv}')

        # 16. iframe structure for private stripe like p-numberInput
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[name^='__privateStripeFrame']"))
        )

        # 17. data insert
        self.wait.until(EC.visibility_of_element_located((By.ID, "payment-numberInput"))).send_keys(number)
        self.wait.until(EC.visibility_of_element_located((By.ID, "payment-expiryInput"))).send_keys(expiry_date)
        self.wait.until(EC.visibility_of_element_located((By.ID, "payment-cvcInput"))).send_keys(cvv)

        # 18. checkbox - I accept terms of...
        # 18a. back from iframe Stripe !
        self.driver.switch_to.default_content()

        #18b: hide blocking banner AGAIN
        try:
            banner = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "demo_store"))
            )
            self.driver.execute_script("arguments[0].style.display='none';", banner)
        except:
            pass

        checkbox = self.wait.until(
            EC.element_to_be_clickable((By.ID, "terms"))  )

        # 18.c - adding scroll to checkbox
        self.driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)

        if not checkbox.is_selected():
            checkbox.click()

        # 19. click button
        self.wait.until(EC.element_to_be_clickable((By.ID, 'place_order'))).click()

    def check_order(self):
        # 20. check excepted result - order number
        order_number = ""
        self.wait.until(EC.url_contains(order_number))
        current_url = self.driver.current_url
        self.assertIn(order_number, current_url)
        print(f' Numer zamowienia to : {order_number}')

    # @unittest.skip("Temporary skipping")
    def test_buy_coupon_payment(self):
        self.add_products_to_cart()
        self.apply_coupon()
        self.go_to_payment()
        self.fill_user_data()
        self.make_payment()
        self.check_order()