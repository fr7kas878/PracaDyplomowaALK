from tests.Selenium_tests.happy_path.base_test import BaseTest

from data.userdata import DataToLogIn

from pages.my_account_page import MyAccountPage


class BaseLogIn(BaseTest):

    def setUp(self):

        super().setUp()

        self.my_account = MyAccountPage(
            self.driver
        )

    def login(self):

        self.my_account.login(
            DataToLogIn.DATA1_USEREXISTINGEMAIL,
            DataToLogIn.DATA1_PASSWORD
        )


class LogToMyAccount(BaseLogIn):

    def test_login_existingaccount(self):

        self.login()

        self.assertTrue(
            self.my_account.is_logged_in()
        )


class LogOut(BaseLogIn):

    def test_logOut(self):

        #first go to login -> call actions from def login
        self.login()

        #6.check expected result - link to log out is displayed
        self.assertTrue(
            self.my_account.is_logged_in()
        )

        #7.click button "Wyloguj" to log out
        self.my_account.logout()

        #8.check expected result - user is logged out
        self.assertTrue(
            self.my_account.is_logged_out()
        )

        self.assertIn(
            "moje-konto",
            self.driver.current_url
        )