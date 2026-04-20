from playwright.sync_api import sync_playwright


URL = "https://fakestore.testelka.pl/"


def test_chromium_responsiveness():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1366, "height": 768})

        page.goto(URL)
        page.screenshot(path="chromium_home.png")

        assert page.title() != ""

        browser.close()


def test_firefox_responsiveness():
    with sync_playwright() as p:
        browser = p.firefox.launch()
        page = browser.new_page(viewport={"width": 1366, "height": 768})

        page.goto(URL)
        page.screenshot(path="firefox_home.png")

        assert page.title() != ""

        browser.close()


def test_webkit_safari_responsiveness():
    with sync_playwright() as p:
        browser = p.webkit.launch()
        page = browser.new_page(viewport={"width": 1366, "height": 768})

        page.goto(URL)
        page.screenshot(path="webkit_home.png")

        assert page.title() != ""
