from selenium.webdriver.common.by import By
from FakeStoreTESTS.data.userdata import UserData
from selenium.webdriver.support import expected_conditions as EC
from FakeStoreTESTS.Selenium_tests.happy_path.base_test import BaseTest
import csv
import os


class BuyingHP(BaseTest):

    def setUp(self):
        super().setUp()

    def test_payment_error(self):

        def safe_hide_banner():
            try:
                self.driver.execute_script("""
                    let el = document.querySelector('.woocommerce-store-notice');
                    if (el) { el.style.display='none'; }
                """)
            except:
                pass

        # 1. primary menu on main page - click Sklep
        safe_hide_banner()
        self.driver.find_element(By.XPATH, '//*[@id="menu-item-198"]').click()

        # 2. choose a first category - windsurfing[1]
        element = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/ul/li[1]//a'))
        )
        element.click()

        # 3. add to cart several products
        products = ["386", "393", "391", "4116", "389"]

        for product_id in products:

            safe_hide_banner()

            element = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-product_id="{product_id}"]'))
            )

            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

            try:
                element.click()
            except:
                self.driver.execute_script("arguments[0].click();", element)

        # 4.click button "Zobacz koszyk" to go to cart
        safe_hide_banner()

        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.added_to_cart.wc-forward'))
        ).click()

        # 5. enter a coupon code and click a button "Zastosuj kupon"
        file_path = os.path.join(os.path.dirname(__file__), '../../data/couponsTest.csv')

        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            coupon_code = rows[7][0]

        print(f' W tym tescie wybieramy kod dla kategorii windsurfing " {coupon_code} "- test pozytywny')

        self.wait.until(
            EC.visibility_of_element_located((By.NAME,'coupon_code')) ).send_keys(coupon_code)
        self.wait.until(
            EC.element_to_be_clickable((By.NAME,'apply_coupon'))  ).click()

        message_element = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME,'woocommerce-message'))  )
        actual_msg = message_element.text
        self.assertIn('Kupon został pomyślnie użyty', actual_msg)

        # 12. Click a button "przejdz do platnosci"
        safe_hide_banner()
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.checkout-button.button.alt.wc-forward')) ).click()

        #13. Check expected result - redirecting to subpage .../zamowienie/
        self.wait.until(EC.url_contains('zamowienie'))
        current_url = self.driver.current_url
        self.assertEqual(current_url, "https://fakestore.testelka.pl/zamowienie/")

        #14. Fulfill an order data
        self.driver.find_element(By.ID,'billing_email').send_keys(UserData.DATA_EMAIL)
        self.driver.find_element(By.ID,'billing_first_name').send_keys(UserData.DATA_FIRST_NAME)
        self.driver.find_element(By.ID,'billing_last_name').send_keys(UserData.DATA_LAST_NAME)
        self.driver.find_element(By.ID,'billing_address_1').send_keys(UserData.DATA_STREET)
        self.driver.find_element(By.ID,'billing_postcode').send_keys(UserData.DATA_POSTAL_CODE)
        self.driver.find_element(By.ID,'billing_city').send_keys(UserData.DATA_CITY)
        self.driver.find_element(By.ID,'billing_phone').send_keys(UserData.DATA_PHONE)

        #15. Fake card payment data form csv
        file_path = os.path.join(os.path.dirname(__file__), '../../data/credit_cards.csv')

        with open(file_path, newline='') as csvfile:
            reader = list(csv.DictReader(csvfile))
            row = reader[5]

            number = row["number"]
            expiry_date = row["expiry_date"]
            cvv = row["cvv"]

            self.wait.until(
                EC.frame_to_be_available_and_switch_to_it(
                    (By.CSS_SELECTOR, "iframe[name^='__privateStripeFrame']")  ))
            print(f'W tym teście wybrano kartę: {number}, {expiry_date}, {cvv}')

            self.wait.until(
                EC.visibility_of_element_located((By.ID, "payment-numberInput"))  ).send_keys(number)
            self.wait.until(
                EC.visibility_of_element_located((By.ID, "payment-expiryInput")) ).send_keys(expiry_date)
            self.wait.until(
                EC.visibility_of_element_located((By.ID, "payment-cvcInput"))  ).send_keys(cvv)
        self.driver.switch_to.default_content()

        # 18. checkbox - I accept terms of...
        safe_hide_banner()

        checkbox = self.wait.until(
            EC.element_to_be_clickable((By.ID, "terms"))
        )
        if not checkbox.is_selected():
            try:
                checkbox.click()
            except:
                self.driver.execute_script("arguments[0].click();", checkbox)

        #19. click button
        safe_hide_banner()
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.wait.until(
            EC.element_to_be_clickable((By.ID, 'place_order'))  ).click()

        #20. Check expected results
        error_element = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "woocommerce-error")) )
        error_text = error_element.text

        self.assertTrue("przeszłości." in error_text or "expiry" in error_text.lower())
        self.assertEqual(self.driver.current_url, "https://fakestore.testelka.pl/zamowienie/")