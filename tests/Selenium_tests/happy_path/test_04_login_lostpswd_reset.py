from faker import Faker

from data.userdata import DataToLogIn

from pages.my_account_page import MyAccountPage

from tests.Selenium_tests.happy_path.base_test import BaseTest


class LostPasswordReset(BaseTest):

    def setUp(self):

        super().setUp()

        self.faker = Faker()

        self.my_account = MyAccountPage(
            self.driver
        )

    # @unittest.skip("Temporary skipping")
    def test_login_lostpassword_reset(self):

        #1.login with wrong password
        self.my_account.login(
            DataToLogIn.DATA1_USEREXISTINGEMAIL,
            self.faker.password()
        )

        #2.check expected result - error text
        error = (
            self.my_account.get_login_error()
        )

        #2a.check if error message contains wrong password
        self.assertIn(
            "nieprawidłowe hasło",
            error.lower()
        )

        #3.click button Resetuj haslo
        self.my_account.open_reset_password()

        #4.enter user login
        self.my_account.reset_password(
            DataToLogIn.DATA1_USEREXISTINGEMAIL
        )

        #5.check expected result - redirect page
        self.assertTrue(
            self.my_account.reset_link_sent()
        )