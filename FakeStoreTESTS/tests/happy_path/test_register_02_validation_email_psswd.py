from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from faker import Faker
import unittest

from FakeStoreTESTS.data.userdata import *


class RegisterValidateFields(unittest.TestCase):
    def setUp(self):
        self.faker = Faker()
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get("https://fakestore.testelka.pl")
        # close a banner if appears
        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "woocommerce-store-notice__dismiss-link"))
            ).click()
        except:
            pass  # if there is no banner - ignore it

    # @unittest.skip("Temporary skipping")
    #@unittest.skip("Temporary skipping")
    #case1 - browser  wrong email validation when password is corret
    def test_invalid_email_browser_validation(self):
        driver = self.driver

        # 1. page Moje konto (menu)
        driver.find_element(By.XPATH, '//*[@id="menu-item-201"]').click()

        #2. email wrong @@
        email_input = driver.find_element(By.ID, 'reg_email')
        email_input.send_keys(DataToLogIn.DATA2_WRONGEMAIL)
        #3. when password is correct
        driver.find_element(By.ID, 'reg_password').send_keys(UserData.DATA_PASSWORD)
        # klick register button
        driver.find_element(By.CLASS_NAME, "woocommerce-form-register__submit").click()

        # check if browser validation message is appearing - this is a construction for browser validator in JavaScript,
        #because we ask a browser tooltip directly, not a running selenium webdriver by searching elements
        validation_message = driver.execute_script(
            "return arguments[0].validationMessage;", email_input
        )

        # 6. check if browser validation message is not empty
        self.assertTrue(len(validation_message) > 0)


    # case2 - browser validation - to short password
    def test_short_password_validation(self):
        driver = self.driver

        driver.find_element(By.XPATH, '//*[@id="menu-item-201"]').click()
        driver.find_element(By.ID, 'reg_email').send_keys(self.faker.email())
        driver.find_element(By.ID, 'reg_password').send_keys("123")

         #only check the password strnght - without registration
        password_strength = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".woocommerce-password-strength")
            )
        )
        #check if text contains word slabe
        self.assertIn("słabe", password_strength.text.lower())


    def tearDown(self):
        self.driver.quit()