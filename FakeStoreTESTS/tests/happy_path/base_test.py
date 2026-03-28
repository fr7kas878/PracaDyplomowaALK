from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import unittest


class BaseTest(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 5)

        self.driver.get("https://fakestore.testelka.pl")

        # close banner if appears
        try:
            self.wait.until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, "woocommerce-store-notice__dismiss-link") # button name on banner is Ukryj
                )
            ).click()
        except:
            pass
    #added has attribute "driver" -> because of chrome unstability
    def tearDown(self):
        if hasattr(self, "driver"):
            self.driver.quit()