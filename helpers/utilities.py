from faker import Faker
from selenium.webdriver.common.by import By

faker = Faker()

def generate_email():
    return faker.email()

def generate_password():
    return faker.password()

class UIHelpers:

    def __init__(self, driver):
        self.driver = driver

    def hide_banner(self):
        # noinspection PyBroadException
        try:
            banner = self.driver.find_element(By.CLASS_NAME, "demo_store")
            self.driver.execute_script("arguments[0].style.display='none';", banner)
        except:
            pass