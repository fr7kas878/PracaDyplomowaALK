# PracaDyplomowaALK

Testy Selenium w Pythonie

Ten projekt zawiera zestaw testów automatycznych dla sklepu https://fakestore.testelka.pl/ (wersja DEMO) , napisanych w Pythonie z użyciem Selenium WebDriver. Testy mają na celu weryfikację kluczowych funkcjonalności w ścieżce zakupowej, takich jak: 
1. Rejestracja i logowanie użytkownika
2. Wyszukiwanie produktów
3. Dodawanie produktów do koszyka
4. Testy płatności z użyciem testowych kart płatniczych 
5. Testy kuponów rabatowych 
6. Walidacje komunikatów dla formularzy i działania przycisków

# WARUNKI WSTĘPNE: 

# URUCHAMIANIE TESTÓW:

# STRUKTURA PROJEKTU:

├── assets
│   └── style.css
├── chromium_home.png
├── data
│   ├── couponsTest.csv
│   ├── credit_cards.csv
│   └── userdata.py
├── firefox_home.png
├── helpers
│   ├── UIHelpers.py
│   └── utilities.py
├── ipad_mini_home.png
├── iphone14.png
├── pages
│   ├── MyAccountPage.py
├── README.md
├── report.html
├── requirements.txt
├── test_results.txt
├── TESTS
│   ├── Playwright_tests
│   │   ├── chromium_home.png
│   │   ├── firefox_home.png
│   │   ├── __init__.py
│   │   ├── ipad_mini_home.png
│   │   ├── iphone14.png
│   │   ├── responsiveness
│   │   │   ├── test_14_desktop_3browsers.py
│   │   │   ├── test_15_mobile_iphone14ProMax.py
│   │   │   └── test_16_tablet_iPadMini.py
│   │   ├── setup_playwright.sh
│   │   └── webkit_home.png
│   └── Selenium_tests
│       ├── happy_path
│       │   ├── base_test.py
│       │   ├── test_01_register_happyPath.py
│       │   ├── test_02_register_validation_email_psswd.py
│       │   ├── test_03_login_myaccount_happyPath.py
│       │   ├── test_04_login_lostpswd_reset.py
│       │   ├── test_05_buyCouponPayment_happyPath.py
│       │   ├── test_09_usingWishlistOptions.py
│       │   ├── test_11_Pricesofproducts.py
│       │   └── test_12_zeroQtyUpdateCart.py
│       ├── __init__.py
│       ├── negative
│       │   ├── test_06_buyCouponPayment-randomCoupon.py
│       │   ├── test_07_couponExpired.py
│       │   ├── test_08_payment_error.py
│       └── test_results.txt



