from selenium.webdriver.common.by import By
from FakeStoreTESTS.data.userdata import UserData
from selenium.webdriver.support import expected_conditions as EC
from FakeStoreTESTS.Selenium_tests.happy_path.base_test import BaseTest
import csv
import os


class BuyingHP(BaseTest):

    def setUp(self):
        super().setUp()

    # @unittest.skip("Temporary skipping")
    def test_payment_error(self):
        # 1. primary menu on main page - click Sklep
        self.driver.find_element(By.XPATH, '//*[@id="menu-item-198"]').click()
        # 2. choose a first category - windsurfing[1]
        element = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/ul/li[1]//a')) )
        element.click()

        # 3. add to cart several products
        #adding several products in a loop by product_id :
        products = ["386", "393", "391", "4116", "389"]
        for product_id in products:
            self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-product_id="{product_id}"]'))).click()

        # 4.click button "Zobacz koszyk" to go to cart
        self.wait.until(
            EC.element_to_be_clickable
            ((By.CSS_SELECTOR, '.added_to_cart.wc-forward'))).click()
        # 5. enter a coupon code and click a button "Zastosuj kupon"
        # 6. use coupons from csv file
        file_path = os.path.join(os.path.dirname(__file__), '/FakeStoreTESTS/data/couponsTest.csv')

        # 7. take a valid code for this category
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile) # tu jest zwykly reader csv - ktory bierze liste a nie slownik
            rows = list(reader)
            coupon_code =rows[7][0]

        print (f' W tym tescie wybieramy kod dla kategorii windsurfing " {coupon_code} "- test pozytywny')
        #8. wait to insert a code
        self.wait.until(
            EC.visibility_of_element_located((By.NAME,'coupon_code'))).send_keys(coupon_code)
        #9. click apply a coupon
        self.wait.until(
            EC.element_to_be_clickable((By.NAME,'apply_coupon'))).click()
        #10 - check displayed message
        message_element = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME,'woocommerce-message' )) )
        #11. Check an expected result:
        actual_msg = message_element.text
        self.assertIn('Kupon został pomyślnie użyty', actual_msg)

        # 12. Click a button "przejdz do platnosci"
        self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'checkout-button.button.alt.wc-forward'))).click()
        #13. Check expected result - redirecting to subpage .../zamowienie/
        self.wait.until(EC.url_contains('zamowienie'))
        current_url = self.driver.current_url
        self.assertEqual(current_url, "https://fakestore.testelka.pl/zamowienie/")
        #14. Fulfill an order data
        #14a. email - from email generator
        generated_email = UserData.DATA_EMAIL
        self.driver.find_element(By.ID,'billing_email').send_keys(generated_email)
        #14b. Name
        firstname = UserData.DATA_FIRST_NAME
        self.driver.find_element(By.ID, 'billing_first_name').send_keys(firstname)
        #14c. Lastname
        lastname = UserData.DATA_LAST_NAME
        self.driver.find_element(By.ID, 'billing_last_name').send_keys(lastname)
        #14d. Street
        street = UserData.DATA_STREET
        self.driver.find_element(By.ID, 'billing_address_1').send_keys(street)
        #14.e Postal code
        postalcode = UserData.DATA_POSTAL_CODE
        self.driver.find_element(By.ID, 'billing_postcode').send_keys(postalcode)
        #14.f City
        city = UserData.DATA_CITY
        self.driver.find_element(By.ID, 'billing_city').send_keys(city)
        #14.g phone_number
        phone = UserData.DATA_PHONE
        self.driver.find_element(By.ID, 'billing_phone').send_keys(phone)
        #15 FAKE CARD PAYMENT DATA

        file_path = '/FakeStoreTESTS/data/credit_cards.csv'

        with open(file_path, newline='') as csvfile:
            reader = list(csv.DictReader(csvfile))
            row = reader[5]  # row7 (index 6, because counting from 0)

            number = row["number"]
            expiry_date = row["expiry_date"]
            cvv = row["cvv"]
            # 16. iframe structure for private stripe like p-numberInput
            self.wait.until(EC.frame_to_be_available_and_switch_to_it( (By.CSS_SELECTOR, "iframe[name^='__privateStripeFrame']")))

            print(f'W tym teście wybrano kartę kredytową o nieprawidowym numerze cvv i data waznosci, ktora juz minela( test negatywny): {number}, {expiry_date}, {cvv}')

        # 17. data insert
            self.wait.until( EC.visibility_of_element_located((By.ID, "payment-numberInput")) ).send_keys(number)
            self.wait.until( EC.visibility_of_element_located((By.ID, "payment-expiryInput")) ).send_keys(expiry_date)
            self.wait.until( EC.visibility_of_element_located((By.ID, "payment-cvcInput")) ).send_keys(cvv)

        # 18. checkbox - I accept terms of...
            # back from iframe Stripe !
            self.driver.switch_to.default_content()
            # click checkbox
            checkbox = self.wait.until(
                EC.element_to_be_clickable((By.ID, "terms")))
            if not checkbox.is_selected():
                checkbox.click()
         #19. click button
            self. wait.until (EC.element_to_be_clickable((By.ID, 'place_order'))).click()


        #20. Check expected results - card is expired, order number is not generated in url:
        error_element = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "woocommerce-error")) )
        error_text = error_element.text

        self.assertTrue( "przeszłości." in error_text or "expiry" in error_text.lower())
        self.assertEqual( self.driver.current_url,"https://fakestore.testelka.pl/zamowienie/")











