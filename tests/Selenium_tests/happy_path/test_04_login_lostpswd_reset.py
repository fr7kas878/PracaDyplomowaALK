from selenium.webdriver.common.by import By
from faker import Faker
from data.userdata import DataToLogIn
from TESTS.Selenium_tests.happy_path.base_test import BaseTest
from selenium.webdriver.support import expected_conditions as EC

class LostPasswordReset(BaseTest):
    def setUp(self):
        super().setUp()
        self.faker = Faker()

    # @unittest.skip("Temporary skipping")
    def test_login_lostpassword_reset(self):
        # 1.page Moje konto (menu)
        self.driver.find_element(By.XPATH, '//*[@id="menu-item-201"]').click()
        # 2.email
        self.driver.find_element(By.ID, 'username').send_keys(DataToLogIn.DATA1_USEREXISTINGEMAIL)
        # 3.password-get random from faker - uncorrect
        self.driver.find_element(By.ID, 'password').send_keys(self.faker.password())
        # 4.click show password
        self.driver.find_element(By.CLASS_NAME, 'show-password-input').click()
        # 5.click button "Zaloguj"
        self.driver.find_element(By.CLASS_NAME,'woocommerce-form-login__submit').click()
        # 6.check expected result - error text
        self.driver.find_element(By.CSS_SELECTOR, ".woocommerce-error")
        # 6a - check if error message contains "nieprawidlowe haslo"
        error = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "woocommerce-error"))
        )
        self.assertTrue(error.is_displayed())
        self.assertIn("nieprawidłowe hasło", error.text.lower())
       # 7.click button "Resetuj haslo"
        self.driver.find_element(By.LINK_TEXT, "Nie pamiętasz hasła?").click()

        #8. enter user login
        self.driver.find_element(By.ID, 'user_login').send_keys(DataToLogIn.DATA1_USEREXISTINGEMAIL)
        # 9. klick button "Resetuj haslo"
        self.driver.find_element(By.CSS_SELECTOR, 'button[value="Resetuj hasło"]').click()
        # 9a. redirecting to reset link page
        self.wait.until(EC.url_contains("reset-link-sent=true"))

        # 10. check the page link - confirm reset link sent = true
        self.assertIn(
            "reset-link-sent=true",
            self.driver.current_url
        )