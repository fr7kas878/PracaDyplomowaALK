from data.userdata import UserData
from pages.my_account_page import MyAccountPage
from selenium.webdriver.common.by import By

from tests.Selenium_tests.happy_path.base_test import BaseTest


class RegisterNewUser(BaseTest):

    LOGOUT_LINK = (
        By.LINK_TEXT,
        "Wyloguj się"
    )

    def setUp(self):
        super().setUp()

        self.page = MyAccountPage(
            self.driver
        )

    def logout(self):

        try:
            self.wait.until(
                lambda d: d.find_element(*self.LOGOUT_LINK)
            ).click()
        except:
            pass

    def test_newuser_registration(self):

        email = self.faker.email()

        self.page.register_new_user(
            email,
            UserData.DATA_PASSWORD
        )

        self.assertTrue(
            self.page.registration_successful()
        )

        self.logout()

    def test_existing_user_registration(self):

        email = self.faker.email()

        # 1. first registration
        self.page.register_new_user(
            email,
            UserData.DATA_PASSWORD
        )

        self.assertTrue(
            self.page.registration_successful()
        )

        self.logout()

        # 2. second attempt (same email)
        self.page.register_new_user(
            email,
            UserData.DATA_PASSWORD
        )

        # expected: still on form OR error visible
        self.assertFalse(
            self.page.registration_successful()
        )