from selenium.webdriver.common.by import By
from FakeStoreTESTS.data.userdata import *
from selenium.webdriver.support import expected_conditions as EC
from FakeStoreTESTS.Selenium_tests.happy_path.base_test import BaseTest
from faker import Faker


class RegisterNewUser(BaseTest):

    def setUp(self):
        super().setUp()
        self.faker = Faker()

        # close the first banner, if appears
        try:
            self.wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, "woocommerce-store-notice__dismiss-link"))
            ).click()
        except:
            pass  # if it's no banner, ignore it

   # @unittest.skip("Temporary skipping")
    def test_newuser_registration(self):
        #1.page Moje konto (menu)
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="menu-item-201"]'))  ).click()

        # check if a banner appears after refreshing web - it caused previous errors
        try:
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "woocommerce-store-notice"))  )
            self.driver.execute_script(
                "document.querySelector('.woocommerce-store-notice')?.remove();"  )
        except:
            pass

        #wait for registration form
        self.wait.until(
            EC.visibility_of_element_located((By.ID, 'reg_email'))  )

        #1. generate email with Faker
        email = self.faker.email()

        #2. insert email
        self.wait.until(
            EC.visibility_of_element_located((By.ID, 'reg_email'))  ).send_keys(email)

        #3.password
        self.driver.find_element(By.ID, 'reg_password').send_keys(UserData.DATA_PASSWORD)

        #4.click show password
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Pokaż hasło"]'))  ).click()

        #4a wait for hide password
        self.wait.until(
            EC.element_to_be_clickable((By.ID, 'reg_password'))  )

        #5.klick register button
        button = self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "woocommerce-form-register__submit"))  )
        button.click()

        #6.Check expected result: registration succeed when link "Delete account" appears on page Moje konto
        element = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "delete-me")) )
        self.assertTrue(element.is_displayed())