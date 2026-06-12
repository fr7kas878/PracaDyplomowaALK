from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.home_page import HomePage

from tests.Selenium_tests.happy_path.base_test import BaseTest


class ProductsInCart(BaseTest):

    PRODUCTS = [
        "386",
        "393",
        "391",
        "4116",
        "389"
    ]

    CATEGORY = (
        By.CSS_SELECTOR,
        "#main ul li:first-child a"
    )

    CART_BUTTON = (
        By.CSS_SELECTOR,
        ".added_to_cart.wc-forward"
    )

    CART_FORM = (
        By.CSS_SELECTOR,
        ".woocommerce-cart-form"
    )

    QUANTITY = (
        By.CSS_SELECTOR,
        "input.qty"
    )

    UPDATE_CART = (
        By.NAME,
        "update_cart"
    )

    OVERLAY = (
        By.CSS_SELECTOR,
        ".blockUI.blockOverlay"
    )

    def setUp(self):

        super().setUp()

        self.home_page = HomePage(
            self.driver
        )

    def add_products(self):

        #1.primary menu on main page - click Sklep
        self.home_page.open_shop()

        #2.choose category - windsurfing
        self.wait.until(
            EC.element_to_be_clickable(
                self.CATEGORY
            )
        ).click()

        self.home_page.hide_banner()

        #3.add products
        for product_id in self.PRODUCTS:

            self.home_page.hide_banner()

            locator = (
                By.CSS_SELECTOR,
                f'[data-product_id="{product_id}"]'
            )

            element = self.wait.until(
                EC.element_to_be_clickable(
                    locator
                )
            )

            self.home_page.scroll_to(
                element
            )

            element.click()

            self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        ".added_to_cart"
                    )
                )
            )

    def open_cart(self):

        self.home_page.hide_banner()

        self.wait.until(
            EC.element_to_be_clickable(
                self.CART_BUTTON
            )
        ).click()

        self.home_page.hide_banner()

        self.wait.until(
            EC.presence_of_element_located(
                self.CART_FORM
            )
        )

    def test_add_to_cart(self):

        self.add_products()

        self.open_cart()

        #4.check expected result
        quantities = self.wait.until(
            EC.presence_of_all_elements_located(
                self.QUANTITY
            )
        )

        total_qty = sum(
            int(
                q.get_attribute(
                    "value"
                )
            )
            for q in quantities
        )

        self.assertEqual(
            total_qty,
            len(
                self.PRODUCTS
            )
        )

        #5.set quantity to 0
        qty_input = self.wait.until(
            EC.presence_of_element_located(
                self.QUANTITY
            )
        )

        self.home_page.scroll_to(
            qty_input
        )

        qty_input.clear()

        qty_input.send_keys(
            "0"
        )

        self.home_page.hide_banner()

        #6.click update
        self.wait.until(
            EC.element_to_be_clickable(
                self.UPDATE_CART
            )
        ).click()

        #7.wait for refresh
        self.wait.until(
            EC.invisibility_of_element_located(
                self.OVERLAY
            )
        )

        self.wait.until(
            EC.staleness_of(
                qty_input
            )
        )

        updated_input = self.wait.until(
            EC.presence_of_element_located(
                self.QUANTITY
            )
        )

        # 8.check expected result - application restores minimal quantity
        self.assertEqual(
            updated_input.get_attribute(
                "value"
            ),
            "1"
        )