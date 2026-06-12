from data.userdata import UserData

from pages.my_account_page import MyAccountPage
from tests.Selenium_tests.happy_path.base_test import BaseTest


class RegisterNewUser(BaseTest):


    def test_new_user_registration(self):


        self.home_page.open_my_account()

        account = MyAccountPage(
            self.driver
        )

        email = self.faker.email()

        account.register_new_user(
            email=email,
            password=UserData.DATA_PASSWORD
        )

        self.assertTrue(
            account.registration_successful()
        )

        self.assertEqual(
            f"{self.BASE_URL}/moje-konto/",
            self.driver.current_url
        )