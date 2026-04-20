from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class MyAccountPage:

    MENU = (By.XPATH, '//*[@id="menu-item-201"]')
    EMAIL = (By.ID, "reg_email")
    PASSWORD = (By.ID, "reg_password")
    REGISTER_BTN = (By.CLASS_NAME, "woocommerce-form-register__submit")
    SUCCESS = (By.CLASS_NAME, "delete-me")
    ERROR = (By.CLASS_NAME, "woocommerce-error")
    BANNER_CLOSE = (By.CLASS_NAME, "woocommerce-store-notice__dismiss-link")

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def open(self):
        self.driver.find_element(*self.MENU).click()
        self.close_banner()

    def close_banner(self):
        try:
            banner = self.wait.until(
                EC.presence_of_element_located(self.BANNER_CLOSE)
            )
            self.driver.execute_script("arguments[0].click();", banner)
        except:
            pass

    def ensure_register_form(self):
        # 1. Close banner and clickable menu
        self.driver.find_element(*self.MENU).click()
        self.close_banner()

        # 2. wait for register formular
        self.wait.until(
            EC.presence_of_element_located(self.EMAIL) )
    def register(self, email, password):
        self.ensure_register_form()

        self.driver.find_element(*self.EMAIL).send_keys(email)
        self.driver.find_element(*self.PASSWORD).send_keys(password)
        self.driver.find_element(*self.REGISTER_BTN).click()

    def wait_success(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.SUCCESS)  )

    def wait_error(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.ERROR) )