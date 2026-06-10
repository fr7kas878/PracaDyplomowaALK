import unittest

from faker import Faker
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from pages.home_page import HomePage


class BaseTest(unittest.TestCase):

    BASE_URL = "https://fakestore.testelka.pl"

    def setUp(self):

        options = Options()

        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extensions")

        self.driver = webdriver.Chrome(options=options)

        self.driver.implicitly_wait(3)

        self.wait = WebDriverWait(self.driver, 10)

        self.faker = Faker()

        self.driver.get(self.BASE_URL)

        self.home_page = HomePage(self.driver)

        self.home_page.close_banner()

    def tearDown(self):

        if self.driver:
            self.driver.quit()