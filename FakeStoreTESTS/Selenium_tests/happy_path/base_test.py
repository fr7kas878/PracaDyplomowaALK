from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from faker import Faker
import unittest


class BaseTest(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")

        self.driver = webdriver.Chrome(options=options)
        # longer wait for better stability
        self.wait = WebDriverWait(self.driver, 10)
        self.faker = Faker()
        self.driver.get("https://fakestore.testelka.pl")
        # force stable viewport
        self.driver.maximize_window()
        # zoom 67% for better stability
        self.driver.execute_script("document.body.style.zoom='67%'")

        # close banner if appears
        try:
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "woocommerce-store-notice"))
            )
            self.driver.execute_script("document.querySelector('.woocommerce-store-notice')?.remove();")
        except:
            pass

    # added "has attribute" with param 'driver' -> because of chrome unstability
    def tearDown(self):
        if hasattr(self, "driver"):
            self.driver.quit()