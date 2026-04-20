from FakeStoreTESTS.pages.MyAccountPage import MyAccountPage
from FakeStoreTESTS.data.userdata import *
from selenium.webdriver.common.by import By
from FakeStoreTESTS.Selenium_tests.happy_path.base_test import BaseTest



class RegisterNewUser(BaseTest):

    def setUp(self):
        super().setUp()
        self.page = MyAccountPage(self.driver, self.wait)

    def test_newuser_registration(self):
        email = self.faker.email()

        self.page.register(email, UserData.DATA_PASSWORD)

        element = self.page.wait_success()
        assert element.is_displayed()

        def logout(self):
            try:
                self.driver.find_element(By.LINK_TEXT, "Wyloguj się").click()
            except:
                pass

    def test_existing_user_registration(self):
        email = self.faker.email()

        # 1. first registration
        self.page.register(email, UserData.DATA_PASSWORD)
        self.page.wait_success()

        # 🔴 KLUCZOWE: logout / reset session
        try:
            self.driver.find_element(By.LINK_TEXT, "Wyloguj się").click()
        except:
            pass

        # 2. second attempt
        self.page.open()
        self.page.register(email, UserData.DATA_PASSWORD)

        error = self.page.wait_error()
        assert error.is_displayed()