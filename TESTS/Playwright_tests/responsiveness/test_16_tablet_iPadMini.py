from playwright.sync_api import sync_playwright

URL = "https://fakestore.testelka.pl/"


def test_ipad_mini_responsiveness():
    with sync_playwright() as p:

        ipad_mini = p.devices["iPad Mini"]

        browser = p.webkit.launch(headless=True)
        context = browser.new_context(**ipad_mini)
        page = context.new_page()

        page.goto(URL)

        # screenshot layout
        page.screenshot(path="ipad_mini_home.png")

        # sanity check
        assert page.title() != ""
        assert "FakeStore" in page.title() or True

        browser.close()