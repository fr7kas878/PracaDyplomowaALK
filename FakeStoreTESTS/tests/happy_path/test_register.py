import unittest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
import unittest

from FakeStoreTESTS.data.userdata import *


class RegisterNewUser(unittest.TestCase):
    def setUp(self):

        # Open page my account
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get('https://fakestore.testelka.pl')
        self.driver.implicitly_wait(10)

        # zamknij banner informujacy o tym,ze to sklep testowy -  jeśli istnieje
        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "woocommerce-store-notice__dismiss-link"))
            ).click()
        except:
            pass  # jeśli nie ma banneru, ignoruj

    #@unittest.skip("Temporary skipping")
    def test_newuser_registration(self):
        #1. page Moje konto (menu)
        self.driver.find_element(By.XPATH, '//*[@id="menu-item-201"]').click()

        #2. email
        self.driver.find_element(By.ID, 'reg_email').send_keys(UserData.DATA_EMAIL)

        #3. password
        self.driver.find_element(By.ID, 'reg_password').send_keys(UserData.DATA_PASSWORD)

        #4.show password
        self.driver.find_element(By.CSS_SELECTOR, '[aria-label="Pokaż hasło"]').click()
        #4a wait for hide password
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.ID, 'reg_password'))
        )
        #5.klick register button
        self.driver.find_element(By.CLASS_NAME, "woocommerce-form-register__submit").click()











