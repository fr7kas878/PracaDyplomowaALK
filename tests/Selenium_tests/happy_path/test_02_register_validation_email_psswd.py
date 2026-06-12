from faker import Faker

from data.userdata import UserData
from data.userdata import DataToLogIn

from pages.home_page import HomePage
from pages.my_account_page import MyAccountPage

from tests.Selenium_tests.happy_path.base_test import BaseTest


class RegisterValidateFields(BaseTest):

    def setUp(self):

        super().setUp()

        self.faker = Faker()

        self.home_page = HomePage(
            self.driver
        )

        self.my_account = MyAccountPage(
            self.driver
        )

    # case1 - browser wrong email validation when password is correct
    def test_invalid_email_browser_validation(self):

        #1.page Moje konto (menu)
        self.home_page.open_my_account()

        self.assertTrue(
            self.home_page.is_my_account_opened()
        )

        #2.email wrong
        self.my_account.fill_registration_form(
            DataToLogIn.DATA_WRONGEMAIL,
            UserData.DATA_PASSWORD
        )

        #3.register
        self.my_account.click_register()

        #4.browser validation
        validation_message = (
            self.my_account.get_email_validation_message()
        )

        #5.check if browser validation message is not empty
        self.assertNotEqual(
            validation_message,
            ""
        )

    # case2 - browser validation - to short password
    def test_short_password_validation(self):

        #1.page Moje konto (menu)
        self.home_page.open_my_account()

        self.assertTrue(
            self.home_page.is_my_account_opened()
        )

        #2.email
        self.my_account.fill_registration_form(
            self.faker.email(),
            "123"
        )

        #3.only check the password strenght
        password_strength = (
            self.my_account.get_password_strength()
        )

        #4.check if text contains word 'slabe'
        self.assertIn(
            "słabe",
            password_strength.lower()
        )