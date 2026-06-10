from data.userdata import UserData
from pages.my_account_page import MyAccountPage
from TESTS.Selenium_tests.happy_path.base_test import BaseTest


class RegisterNewUser(BaseTest):

    def test_new_user_registration(self):
        self.home_page.open_account()

        account = MyAccountPage(
            self.driver
        )

        email = self.faker.email()

        account.register_new_user(
            email=email,
            password=UserData.DATA_PASSWORD
        )

        # ASSERT 1
        self.assertTrue(
            account.registration_successful(),
            "Delete account button is not visible"
        )

        # ASSERT 2
        self.assertEqual(
            f"{self.BASE_URL}/moje-konto/",
            self.driver.current_url,
            "User was not redirected to My Account page"
        )

        # ASSERT 3
        self.assertIn(
            "moje-konto",
            self.driver.current_url
        )

        # ASSERT 4
        self.assertEqual(
            email,
            self.driver.find_element(
                *account.EMAIL
            ).get_attribute("value"),
            "Registered email differs from generated email"
        )

        # ASSERT 5
        self.assertTrue(
            self.driver.find_element(
                *account.DELETE_ACCOUNT
            ).is_displayed(),
            "Delete account button should be visible"
        )

        # ASSERT 6
        self.assertNotIn(
            "error",
            self.driver.page_source.lower(),
            "Unexpected error message displayed"
        )