
from playwright.sync_api import sync_playwright

URL = "https://fakestore.testelka.pl/"

def test_iphone_14_promax_responsiveness():
    with sync_playwright() as p:

        iphone = p.devices["iPhone 14 Pro Max"]

        browser = p.webkit.launch()
        context = browser.new_context(**iphone)
        page = context.new_page()

        page.goto(URL)
        page.screenshot(path="iphone14.png")

        assert page.title() != ""

        browser.close()


def test_ecommerce_sanity_check():
    with sync_playwright() as p:

        browser = p.chromium.launch()
        page = browser.new_page()

        page.goto(URL)
        assert page.title() != ""

        page.click("a.woocommerce-LoopProduct-link")
        assert "product" in page.url

        page.goto(URL + "cart/")
        assert "cart" in page.url

        page.goto(URL + "checkout/")
        assert "checkout" in page.url

        browser.close()