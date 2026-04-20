from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UIHelpers:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def hide_banner(self):
        try:
            self.driver.execute_script("""
                let el = document.querySelector('.woocommerce-store-notice');
                if (el) el.remove();
            """)
        except:
            pass