from selenium.webdriver.common.by import By
from FakeStoreTESTS.data.userdata import *
from happy_path.base_test import BaseTest
from selenium.webdriver.support import expected_conditions as EC


class BaseLogIn(BaseTest):

    def login(self):  # możesz też wydzielić do wspólnej klasy bazowej
        #1.page Moje konto (menu)
        self.driver.find_element(By.XPATH, '//*[@id="menu-item-201"]').click()
        #2.email
        self.driver.find_element(By.ID, 'username').send_keys(DataToLogIn.DATA1_USEREXISTINGEMAIL)
        #3.password
        self.driver.find_element(By.ID, 'password').send_keys(DataToLogIn.DATA1_PASSWORD)
        #4.click show password
        self.driver.find_element(By.CLASS_NAME, 'show-password-input').click()
        #5.click button "Zaloguj"
        self.driver.find_element(By.CLASS_NAME, "woocommerce-form-login__submit").click()
        #5a - check if you are logged properly
        self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "woocommerce-MyAccount-content"))
        )


class LogToMyAccount(BaseLogIn):
    # @unittest.skip("Temporary skipping")
    def login_existingaccount(self):
        self.login()

class LogOut(BaseLogIn):
    def test_logOut(self):
        #first go to login _> call actions from def login
        self.login()

        #6.check expected result - link to log out is displayed
        logout = self.wait.until(
            EC.visibility_of_element_located((By.LINK_TEXT, "Wyloguj")) )
        self.assertTrue(logout.is_displayed())

        #7. click button "Wyloguj" to log out
        self.driver.find_element(By.LINK_TEXT, "Wyloguj").click()

        # 8. check expected result - user is logged out (login form is visible)
        self.wait.until(
            EC.visibility_of_element_located((By.NAME, "login")))
        self.assertIn("moje-konto", self.driver.current_url)