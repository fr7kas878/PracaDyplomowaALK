from selenium.webdriver.common.by import By
from FakeStoreTESTS.Selenium_tests.happy_path.base_test import BaseTest
class PriceTest(BaseTest):
    def test_check_prices(self):
        try:
            product = self.driver.find_element(By.CSS_SELECTOR, "li.product.sale")
            name = product.find_element(By.CSS_SELECTOR, ".woocommerce-loop-product__title").text
            # 1. Get the old price (del) and the new price (ins)
            old_price_raw = product.find_element(By.CSS_SELECTOR, "del .woocommerce-Price-amount").text
            new_price_raw = product.find_element(By.CSS_SELECTOR, "ins .woocommerce-Price-amount").text
            # 2. cut off the currency and normalize formatting to float. \xa0 is space in unicode-UTF8
            old_val = float(old_price_raw.replace("zł", "").replace(",", ".").replace("\xa0", "").replace(" ", "").strip())
            new_val = float(new_price_raw.replace("zł", "").replace(",", ".").replace("\xa0", "").replace(" ", "").strip())
            # 3. Compare prices and create a result message
            if new_val < old_val:
                status = f"PASSED: {name} is on sale. Old: {old_val}, New: {new_val}"
            else:
                status = f"FAILED: {name} price is not lower. Old: {old_val}, New: {new_val}"
            print(status)
            # 4. Save price status differences in file
            with open("test_results.txt", "a", encoding="utf-8") as file:
                file.write(status + "\n")
            # 5. Use assertion to confirm the test pass in unittest
            self.assertTrue(new_val < old_val, f"Sale price {new_val} is not lower than {old_val}")
        except Exception as e:
            self.fail(f"Could not find sale products or prices: {e}")