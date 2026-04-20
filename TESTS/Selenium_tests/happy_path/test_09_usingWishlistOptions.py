from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from TESTS.Selenium_tests.happy_path.test_03_login_myaccount_happyPath import LogToMyAccount

class UsingWishlistOptions(LogToMyAccount):

    def test_addingToWishlist(self):

        # login reused from base class (LogToMyAccount)
        self.login_existingaccount()

        # 1.Go to mainpage and choose category "wspinaczka"
        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'custom-logo'))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH,'//section[contains(@class,"storefront-product-categories")]//a[contains(.,"Wspinaczka")]//img'))).click()

        # 2. click to product
        self.wait.until(EC.element_to_be_clickable((By.XPATH,'//a[contains(@href,"gran-koscielcow")]'))).click()
        # 2a. click "add to wishlist" - if it's not on my wishlist yet
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@class,"add_to_wishlist")]'))).click()
        except:
            pass

        # check expected result : product was added to wishlist
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@href,"wishlist")]'))).click()

        self.assertTrue(
            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//a[contains(@href,"gran-koscielcow")]')
                )
            ).is_displayed(),
            "Product not in wishlist"
        )