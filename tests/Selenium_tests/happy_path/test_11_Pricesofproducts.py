from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from tests.Selenium_tests.happy_path.base_test import BaseTest


class PriceTest(BaseTest):

    SALE_PRODUCT = (
        By.CSS_SELECTOR,
        "li.product.sale"
    )

    PRODUCT_NAME = (
        By.CSS_SELECTOR,
        ".woocommerce-loop-product__title"
    )

    OLD_PRICE = (
        By.CSS_SELECTOR,
        "del .woocommerce-Price-amount"
    )

    NEW_PRICE = (
        By.CSS_SELECTOR,
        "ins .woocommerce-Price-amount"
    )

    RESULT_FILE = "test_results.txt"

    def normalize_price(
            self,
            price
    ):

        return float(

            price

            .replace(
                "zł",
                ""
            )

            .replace(
                ",",
                "."
            )

            .replace(
                "\xa0",
                ""
            )

            .replace(
                " ",
                ""
            )

            .strip()
        )

    def save_result(
            self,
            result
    ):

        with open(
                self.RESULT_FILE,
                "a",
                encoding="utf-8"
        ) as file:

            file.write(
                result + "\n"
            )

    def test_check_prices(self):

        #1.find product on sale
        product = self.wait.until(
            EC.visibility_of_element_located(
                self.SALE_PRODUCT
            )
        )

        #2.get product name
        name = product.find_element(
            *self.PRODUCT_NAME
        ).text

        #3.get old price
        old_price = product.find_element(
            *self.OLD_PRICE
        ).text

        #4.get discounted price
        new_price = product.find_element(
            *self.NEW_PRICE
        ).text

        #5.normalize values
        old_val = self.normalize_price(
            old_price
        )

        new_val = self.normalize_price(
            new_price
        )

        #6.create result message
        status = (
            f"{name} | old: {old_val} | new: {new_val}"
        )

        self.save_result(
            status
        )

        print(
            status
        )

        #7.check expected result
        self.assertLess(
            new_val,
            old_val,
            (
                f"Sale price {new_val} "
                f"is not lower than {old_val}"
            )
        )