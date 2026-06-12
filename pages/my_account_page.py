from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.home_page import HomePage


class MyAccountPage(BasePage):

    EMAIL = (By.ID, "reg_email")
    PASSWORD = (By.ID, "reg_password")

    LOGIN_EMAIL = (By.ID, "username")
    LOGIN_PASSWORD = (By.ID, "password")

    RESET_LOGIN = (By.ID, "user_login")

    SHOW_PASSWORD = (By.CSS_SELECTOR, '[aria-label="Pokaż hasło"]')
    LOGIN_SHOW_PASSWORD = (By.CLASS_NAME, "show-password-input")

    REGISTER = (By.CLASS_NAME, "woocommerce-form-register__submit")
    LOGIN = (By.CLASS_NAME, "woocommerce-form-login__submit")

    RESET_BUTTON = (By.CSS_SELECTOR, 'button[value="Resetuj hasło"]')
    LOST_PASSWORD = (By.LINK_TEXT, "Nie pamiętasz hasła?")

    ERROR = (By.CLASS_NAME, "woocommerce-error")

    DELETE_ACCOUNT = (By.CLASS_NAME, "delete-me")
    PASSWORD_STRENGTH = (By.CSS_SELECTOR, ".woocommerce-password-strength")

    MY_ACCOUNT_CONTENT = (By.CLASS_NAME, "woocommerce-MyAccount-content")
    LOGOUT = (By.LINK_TEXT, "Wyloguj")
    LOGIN_FORM = (By.NAME, "login")

    # 🔥 NOWE: przełącznik rejestracji (ważne!)
    REGISTER_TAB = (By.LINK_TEXT, "Zarejestruj się")

    def register_new_user(self, email, password):

        HomePage(self.driver).open_my_account()
        HomePage(self.driver).close_banner()

        # 🔥 KLUCZOWE: przełącz na rejestrację
        try:
            self.click(self.REGISTER_TAB)
        except:
            pass  # jeśli już widoczna

        self.type(self.EMAIL, email)
        self.type(self.PASSWORD, password)

        self.click(self.SHOW_PASSWORD)
        self.click(self.REGISTER)

        print(self.driver.current_url)
        self.driver.save_screenshot("debug_register.png")

    def fill_registration_form(self, email, password):

        HomePage(self.driver).open_my_account()
        HomePage(self.driver).close_banner()

        try:
            self.click(self.REGISTER_TAB)
        except:
            pass

        self.type(self.EMAIL, email)
        self.type(self.PASSWORD, password)

    def click_register(self):
        self.click(self.REGISTER)

    def get_email_validation_message(self):
        return self.get_validation_message(self.EMAIL)

    def get_password_strength(self):
        return self.get_text(self.PASSWORD_STRENGTH)

    def registration_successful(self):

        try:
            return self.is_visible(self.DELETE_ACCOUNT)
        except:
            return False

    def login(self, email, password):

        HomePage(self.driver).open_my_account()

        self.type(self.LOGIN_EMAIL, email)
        self.type(self.LOGIN_PASSWORD, password)

        self.click(self.LOGIN_SHOW_PASSWORD)
        self.click(self.LOGIN)

    def is_logged_in(self):
        return self.is_visible(self.MY_ACCOUNT_CONTENT)

    def logout(self):
        self.click(self.LOGOUT)

    def is_logged_out(self):
        return self.is_visible(self.LOGIN_FORM)

    def get_login_error(self):
        return self.get_text(self.ERROR)

    def open_reset_password(self):
        self.click(self.LOST_PASSWORD)

    def reset_password(self, email):
        self.type(self.RESET_LOGIN, email)
        self.click(self.RESET_BUTTON)

    def reset_link_sent(self):
        return "reset-link-sent=true" in self.driver.current_url