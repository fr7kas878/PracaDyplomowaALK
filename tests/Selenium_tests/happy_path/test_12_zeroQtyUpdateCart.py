from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from TESTS.Selenium_tests.happy_path.base_test import BaseTest


class ProductsInCart(BaseTest):

    def setUp(self):
        super().setUp()

    # @unittest.skip("Temporary skipping")
    def test_add_to_cart(self):
        # 1. primary menu on main page - click Sklep
        self.driver.find_element(By.XPATH, '//*[@id="menu-item-198"]').click()

        # 2. choose a first category - windsurfing[1]
        element = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/ul/li[1]//a'))
        )
        element.click()

        # hide banner after navigation
        self.ui.hide_banner()

        # 3. add to cart several products --> adding several products in a loop by product_id :
        products = ["386", "393", "391", "4116", "389"]

        for product_id in products:

            # 3a. hide banner before each click
            self.ui.hide_banner()

            element = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-product_id="{product_id}"]'))
            )
            element.click()

            # wait for AJAX confirmation (product added)
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".added_to_cart"))
            )

        # 3.b hide banner before going to cart
        self.ui.hide_banner()

        # 4. click button "Zobacz koszyk" to go to cart
        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.added_to_cart.wc-forward'))
        ).click()

        # 4a. hide banner on cart page
        self.ui.hide_banner()

        # 5. check expected result -> summary ordered quantity of products
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".woocommerce-cart-form"))
        )

        quantities = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".qty"))
        )

        total_qty = sum(int(q.get_attribute("value")) for q in quantities)

        self.assertEqual(total_qty, len(products))

        # 6. set quantity of product to 0
        qty_input = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.qty"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", qty_input)
        qty_input.clear()
        qty_input.send_keys("0")

        # 6a.hide banner
        self.ui.hide_banner()

        # 7. Click button "Zaktualizuj koszyk"
        update_btn = self.wait.until(
            EC.element_to_be_clickable((By.NAME, "update_cart")))
        update_btn.click()

        # 7a.wait for cart refresh
        self.wait.until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".blockUI.blockOverlay")))


        self.wait.until(
             EC.presence_of_element_located((By.CSS_SELECTOR, ".woocommerce-cart-form")) )

        # 8. Check expected result - product is not visible in cart anymore
        self.wait.until(
            EC.staleness_of(qty_input)   )

        updated_input = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.qty"))  )

        self.assertEqual(updated_input.get_attribute("value"), "0")