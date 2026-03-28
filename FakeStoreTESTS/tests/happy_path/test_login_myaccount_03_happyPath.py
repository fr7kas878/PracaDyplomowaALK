from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from faker import Faker
import unittest

from FakeStoreTESTS.data.userdata import *


class LogToMyAccount(unittest.TestCase):
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

    def test_login_existingaccount(self):


    # case - log to my account - happy path
        #1.page Moje konto (menu)
        self.driver.find_element(By.XPATH, '//*[@id="menu-item-201"]').click()
        #2.email
        self.driver.find_element(By.ID, 'username').send_keys(DataToLogIn.DATA1_USEREXISTINGEMAIL)
        #3.password
        self.driver.find_element(By.ID, 'password').send_keys(DataToLogIn.DATA1_PASSWORD)
        #4.click show password
        self.driver.find_element(By.CLASS_NAME, 'show-password-input').click()
        #5.click button "Zaloguj"
        self.driver.find_element(By.CLASS_NAME, "woocommerce-form-login__submit").click()
        #6.check expected result - link to log out is displayed

        logout = WebDriverWait(self.driver, 5).until(
        EC.visibility_of_element_located((By.LINK_TEXT, "Wyloguj"))
        )
        self.assertTrue(logout.is_displayed())
        #7. click button "Wylogujj" to log out
        self.driver.find_element(By.LINK_TEXT, "Wyloguj").click()

    def tearDown(self):
        self.driver.quit()





