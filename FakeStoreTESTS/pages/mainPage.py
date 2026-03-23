"""
Tu maja byc logiki do stron,a nie testy!!!

klasy dla danej strony, metody i scenariusze testowe
logikę stron
klasy reprezentujące strony (np. LoginPage, CartPage)

metody typu:

login()
add_to_cart()
click_checkout()

tests/
 tu musze miec testy właściwe, bo poprzednio mialam zla strukture wg wytycznych modelu obiektowego

scenariusze testowe
asercje (assert)
przypadki happy path / negative

czyli np.:
def test_login_success():
    login_page.login("user", "pass")
    assert home_page.is_logged_in() - sprawdz czy jest zalogowany na stronie
"""
